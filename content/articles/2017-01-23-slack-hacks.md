Title: A Quick Hack for Science Slack
Date: 2017-02-02
Slug: slack-hacks
Summary: I was forced to use PHP and cron jobs to monitor servers. Don't do this.

At STScI, there's a small herd of Linux servers that are used by the research staff for a variety of compute-hungry tasks. (They are creatively named `science1`, `science2`, ..., `scienceN`.)

Since it's a pretty small group using the science cluster, STScI has not yet moved to a job submission system to ensure consistent utilization. Instead, there is an informal agreement to `nice` your batch jobs and not use more than a certain fraction of the resources when others are waiting.

We don't have any automatic enforcement of these rules (since the tool to enforce such restrictions automatically is, in fact, a job submission system). Instead, as of relatively recently, we have a Slack channel called `#sciencecluster` where researchers are encouraged to give their colleagues a heads up when they are heavily loading the servers.

# So, what kind of technological solutions could help?

One advantage of team chat is that you can provide visibility into decisions without explicitly involving everyone in a conversation. GitHub's Hubot takes this to an extreme, where most actions that need to be communicated to a team are actually performed in a team chat window with the concerned parties present (or, at least, subscribed).

Since we're just starting to use Slack at STScI, I thought it would be useful to demonstrate how a custom command could provide useful context for a group.

What I decided on was a `/sciencecluster` command that would display the hostname of the server with the lowest system load in the science cluster. By checking that, researchers would not need to individually SSH in to N servers to compare their load conditions.

![Demo screenshot showing custom command]({attach}2017-01-23-slack-hacks/demo.png)

# How do you monitor servers when you're not working in the IT division and there's no public monitoring infrastructure?

Through a combination of old-school UNIX and some hacky programming! We have a few NFS network mounts at work, including one that exposes `/grp/webpages/<yourname>` at `http://www.stsci.edu/~<yourname>`. The web server has `mod_php` installed. That was enough to cobble together something that can respond to the Slack slash command.

Since I can SSH to our `science*` machines, I can add lines to my `crontab` that run on each machine. I went in to each machine and added (something like) this line to my `crontab`:

    0-59/12 * * * * /user/jlong/science_minion.sh

My `science_minion.sh` script looked like this:

```shell
#!/bin/bash
uptime > "/grp/webpages/jlong/sciencecluster/$(hostname)"
date >> "/grp/webpages/jlong/sciencecluster/$(hostname)"
echo "cpus: $(cat /proc/cpuinfo | grep physical | wc -l)" >> "/grp/webpages/jlong/sciencecluster/$(hostname)"
```

What these two files mean is that every five minutes, on each server, a file named for that server is created (or replaced) in my personal web space. It contains the output of uptime:

```
$ uptime
 15:32:28 up 26 days, 14:25,  5 users,  load average: 0.70, 0.52, 0.46
```

The key here is the "load average", which basically says how many processes are contending for CPU time. On Linux, if you have 16 CPUs and a load average of about 16, everything is hunky-dory. You don't have any jobs waiting for the operating system to pause someone else's process so that they can run.

Of course, `uptime` doesn't tell you how many CPUs you have to load down. We'll get to that in a second.

The second line just adds the current date so that I can know how old the information is. If someone checks the state of the cluster, then starts a bunch of jobs on the least-loaded server, the `/sciencecluster` command will still show that server as the least loaded for about five minutes.

The last line counts the number of physical CPUs (cores) in the server. Yes, it does this every five minutes, even though it's not expected to change. (I said it was a hack!)

The command `cat /proc/cpuinfo | grep "physical id" | wc -l` reads a special system file with information on the CPUs (`/proc/cpuinfo`), filters the lines such that only ones with `physical` are included, and counts how many of those there are. That gives us the denominator we need to normalize the load average (i.e. if we want to compare between a 16 core server and a 32 core server).

Here's the content of `/grp/webpages/jlong/sciencecluster/science7.stsci.edu`:

```
 15:36:01 up 26 days, 14:29,  0 users,  load average: 0.01, 0.01, 0.00
Mon Jan 23 15:36:01 EST 2017
cpus: 32
```

# What about the Slack part?

When you go to the Slack "App Directory", (e.g. from "Settings", "Configure Apps") there is a link in the top right to "Build". I chose to "Make a Custom Integration", specifically a "Slash Command" integration.

If you've built an IRC bot before, you'll be happy to hear that you don't have to manage a stateful connection yourself. In fact, the bot "account" that responded to the slash command in the above screenshot isn't an account at all. The Slack service detects the slash commands you have configured when they're used by your teammates in chat, then makes an HTTP (web) request to a URL you define with the contents of their message.

In this case, all I had at my disposal was PHP. For all its faults, PHP was "good enough" to make a proof of concept. When the URL `http://www.stsci.edu/~jlong/sciencecluster/slack_command.php` is requested by the Slack service, my script supplies an "in-channel" reply with the "best" server based on the 5 minute load averages. Slack then inserts the response message into the channel or conversation where the commmand was used, giving it the origin username "science-minion" and a little "BOT" badge to indicate it's not coming from an actual user.

The script itself is based on a [PHP implementation of a Slack command](https://github.com/mccreath/isitup-for-slack/blob/master/isitup.php) I borrowed from David McCreath (@mccreath) on GitHub under the terms of the MIT license.

Rather than go through my code line-by-line, I'll just describe how I get the monitoring information. I loop over the files in the same directory as the script with names that match a certain pattern in order to find all the load measurements deposited there by my cronjobs. I parse the load info, date string, and CPU count into an array for each server, then loop over these arrays to find the best average load normalized by CPU count. Finally, I assemble the message that gets displayed and encode it as JSON. The conversion to JSON is necessary for messages that get displayed in-channel. (If you want your slash command to remain between the user and your script, you can just echo out a string in response.)

A slightly cleaned-up version of the script is below. I rather dislike PHP, so I reminded myself of *just enough* to get this working. (You have been warned!)

```php
<?php
header('Content-Type: application/json');
# Inspired by / derived from https://github.com/mccreath/isitup-for-slack/blob/master/isitup.php
# by David McCreath (@mccreath)
# under the terms of the MIT license

# Grab some of the values from the slash command, create vars for post back to Slack
$command = $_POST['command'];
$text = $_POST['text'];
$subcommand = trim($command);
$token = $_POST['token'];
$response_url = $_POST['response_url'];

# Check the token and make sure the request is from our team
if($token != 'your-token-here') {
  $msg = "The token for the slash command doesn't match. Check your script.";
  die($msg);
  echo $msg;
}

$stats = array();

foreach (glob("*.stsci.edu") as $filename) {
  $serverstats = array('hostname' => $filename);
  $bits = file($filename);
  // 0: load avg
  preg_match("/load average: ([\d.]+), ([\d.]+), ([\d.]+)/", $bits[0], $matches);
  
  // n.b. $matches[0] will be the entire matched string
  $serverstats['load_last_5_min'] = (float)$matches[2];
  $serverstats['load_last_5_min_display'] = $matches[2];
  // 1: date
  $serverstats['check_date'] = trim($bits[1]);
  // 2: cpu count
  preg_match("/cpus: (\d+)/", $bits[2], $matches);
  $serverstats['cpu_count'] = (int)$matches[1];
  $stats[$filename] = $serverstats;
}

$best = '';
$best_load_avg = 1000.0;
$best_load_avg_cpu_count = 1.0;

foreach ($stats as $hostname=>$serverstats) {
  if ($best === '') {
    $best = $serverstats;
  }
  foreach ($serverstats as $key=>$val) {
    if ($best['load_last_5_min'] / $best['cpu_count'] > $serverstats['load_last_5_min'] / $serverstats['cpu_count']) {
      $best = $serverstats;
    }
  }
}
$hostname = $best['hostname'];
$message = "$hostname has the best normalized 5 minute load average (" . $best['load_last_5_min'] . " / " . $best['cpu_count'] . " cpus as of " . $best['check_date'] . ")";
echo json_encode(array(
  "response_type" => "in_channel",
  "text" => $message,
));
?>
```

# Is this secure?

Unless you think server load information is sensitive, I would say yes. There's no way for the web service to execute commands on any of the science servers. All it does is look at files updated by jobs running (as me) on the science cluster machines and use those to pick the current least-overloaded system. In fact, without the Slack token from the integrations page, the script won't do anything for any request that doesn't come from one of our Slack users.

# Is this a good idea?

No! If we had a dashboard for the science cluster, or some visibility into server load that didn't require cobbling together cron jobs, there would be little need for such an integration.

However, in the circumstances, it does provide useful time savings over SSHing to every machine, running `uptime`, and trying to remember how many cores there are.