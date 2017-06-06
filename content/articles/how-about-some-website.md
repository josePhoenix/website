Title: How about some website?
Date: 2017-06-03
Slug: how-about-some-website
Summary: A pernicious trend afflicts the sciences in which scientists are called upon to make website. In the spirit of harm reduction, I present a primer for fellow researchers.
Status: draft

It has come to my attention that everyone wants a damn web app these days. Because I have only minor reservations about inflicting a new generation of half-baked scientist-designed web applications on the world, I have put together this guide in hopes that I can teach my colleagues just enough to be dangerous.

As with any good tutorial author, I believe that there are certain conceptual distinctions which, if I could only set them down in words, would allow the novice to reason their way out of any web-junk-related quandary they encounter.

# In the beginning there were computers that sent bytes to each other

Well, in the _beginning_ beginning there was a quark-gluon plasma. (Before that, you'll have to ask someone else.) But the early days of networked computing were an extension of the time-honored tradition of hooking up your terminal to a bigger, fancier computer elsewhere by means of an extra-long wire. This worked very well for a long time, provided you were only interested in last month's sales figures that Lance had input on the company mainframe. If you wanted the figures for the European branch of the firm, you had to use [Telex](https://en.wikipedia.org/wiki/Telex) and hope that Marcel looked at the teleprinter before heading home for dinner.

Next came the Internet, which allowed two people with two extra-long wires to use both and log in to big fancy computers twice as far away. At the time, not many people had big fancy computers or extra long wires, so the madness was finite. These days, everyone has a big fancy computer (by the standards of those halcyon days) and the madness is growing proportional to $O(n!)$, where $n$ is the number of people on the planet.

But suppose for a moment that you have access to a single computer, and it in turn has a long wire connecting it to a distant computer. In order to communicate with the machine on the other end, you have to solve several problems. Some of these problems reduce to electrical engineering (which in turn reduces to physics 😇). Others are a matter of manners: who should speak first in a given situation, how to conclude a conversation, asking an intermediary to please forward your invitations, sending and receiving RSVPs, ensuring your conversation partner is alive and responsive. Things like that.

# Protocols

Have you ever considered that the Internet is different from the Web? It's true. I read it on the Internet.

The [Internet protocol](https://en.wikipedia.org/wiki/Internet_Protocol) lets you have a whole variety of conversations over your very long wires. It solves some of the very fundamental etiquette problems with communicating with a distant conversation partner (like routing your messages to the correct destination). Atop this, clever engineers have layered TCP: the Transmission Control Protocol. This allows you to be reasonably sure your conversation partner is alive, so long as they keep acknowledging your messages.

These two protocols underpin every web application you use, but they are not web-specific. They could just as easily be transporting email, or World of Warcraft battle instructions, or Skype video of your friend's cat. However, they do have the concept of a *port*, which bears a quick explanation before we explain the web-specific protocol (HTTP) that we'll be dealing with, which sits atop TCP/IP.

## Ports

The simplest way to send some ones and zeros over a wire is to modulate the voltage on one end and look at the other end with some kind of voltage probe. This is, more or less, what happens on a wired network connection. Fortunately, the networking hardware takes care of the [exact details](https://en.wikipedia.org/wiki/PHY_(chip)). But what if two people want to talk on the line at once? Or you want to use your single wire to both connect to your distant computer and to connect to a yet further computer via the network. You'll get all your [bits](https://www.google.com/search?tbm=isch&q=bacon+bits) mixed up! 

"Better run two wires, I guess," I hear you say. Wrong!

When writing computer applications with networking capabilities, we operate several levels removed from the actual hardware. However, you will still hear about ports. These are an abstraction within your computer's operating system allowing multiple programs (and multiple users) to share the same physical wire (or bit of WiFi spectrum) for their communication needs. A port is denoted by a number (usually from 1-65535). When you contact a remote system (say, to request a page of the latest [dank memes](http://reddit.com/r/me_irl/)), your computer will attempt to connect to a numbered port on the remote system and open a numbered port on your system as the "return address" for your request. Even though your computers only have one physical connection to the network, your operating system ensures that everyone trying to use it gets their messages sent where they need to go.

When you are writing a _service_ (with a _server_, see) you "bind to" a port. This signs your server software up for the responsibility of answering all these requests for dank memes. Connections come in with their return addresses, some information about what they want, and you send memes in return.

Websites (and web applications) are generally made available on port 80. In development, this might be port 8000 or 8080. For web applications served over `https://` (you know, the padlock icon), the port is 443.

High numbered ports like 8000 and 8080 require no special privileges to bind to. However, operating systems typically limit the ability of random programs to bind to port numbers below 1024 for security reasons.

# The Hypertext Transfer Protocol (HTTP)

The Hypertext Transfer Protocol (HTTP) is the language your browser speaks with websites. It specifies the polite way to request things (cat GIFs, web pages, etc.) as well as how to transfer information to the website on the other end (forms to fill out, memes to upload, etc.).

If you'll indulge a brief digression into history (unlike the preceding paragraphs, lol amirite):

Hypertext is a concept dating back to the 1960s (or even the 1940s, though it was not called hypertext then). The central conceit is that words may be _hyperlinked_ to other documents--or sections of other documents--to allow efficient navigation through a _web_ of documents. In 1989, Tim Berners-Lee was working at CERN and thoroughly frustrated with the profusion of incompatible documentation systems. He was aware of hypertext, and developed HTTP (along with the first software that implemented it) as a way of:

> generalising, going to a higher level of abstraction, thinking about all the documentation systems out there as being possibly part of a larger imaginary documentation system.

["Biography and Video Interview of Timothy Berners-Lee at Academy of Achievement". Achievement.org.](http://www.achievement.org/achiever/sir-timothy-berners-lee/#interview).

This invention became the World Wide Web. Fortunately, this has completely solved the problem of disjoint, outdated, poorly curated technical documentation for large engineering projects. (Lol, jk. That was the [wiki](). Right?)

There are three key components of HTTP that need to be understood for a productive career churning out mediocre web applications for unappreciative bosses. (I mean, if you're in to that sort of thing.) They are:

  * **URLs**
  * **Methods** (or **verbs**)
  * **Response codes**

(I debated including the **markup language**, but it's not part of HTTP proper. We'll talk about it later.)

## URLs

URL stands for Uniform Resource Locator. It does what it says. In this context, a "resource" is a web page, an image, a file for download, or some online location backed by a web service. Locator means that it includes enough information for a computer to _automatically_ go and retrieve the resource in response to a mouse click or a linked reference within some document. Uniform means that it follows, more or less, this arrangement:

```
    http://user:password@www.example.com:8000/path/to/resource?name=Shirley&gender=queer%20as%20fuck#about-our-site
```

This example intentionally includes all the bells and whistles; most URLs omit some of these elements. Let's break it down.

### Transport: `http://` (required)

The first part is called the _transport_. It specifies how to get to the resource (i.e. what protocol to use), as well as implying a default port (80 for `http://`, 443 for `https://`).

### Credentials: `user:password@` (optional)

Found infrequently in the wild these days, the specification allows users to incorporate credentials in their links. However, credentials provided this way are treated differently from those submitted from login pages you may be familiar with, making this feature less useful.

### Hostname: `www.example.com` (required)

Extracting meaning from hostnames requires understanding a whole separate subsystem underpining the internet: the Domain Name System. For now, trust that your computer is smart enough to know that `internal.example.com` is actually a human-friendly name for a computer. (It has a computer-friendly name, too: `2606:2800:220:1:248:1893:25c8:1946`. Or `93.184.216.34` if you're living in the past.)

### Port: `:8000` (optional)

As I've mentioned a couple times, this is optional as a default port is inferred from the transport. However, if your service is not running on the default port, you must specify a port number.

### Path: `/path/to/resource` (optional)

Once you get it on its own, doesn't this look like a UNIX file path? Same basic idea. The first web servers mapped URL paths to file system paths by prepending the path to something called a "document root". Say you had all your HTML files in `/srv/www/`. You'd configure your web server to use `/srv/www/` as your document root, so when a request for `http://yoursite.com/things/thing.html` came in the web server would send back the file `/srv/www/things/thing.html`.

These days, paths do not map obviously to file system locations. This is the price we pay for progress, I suppose.

If a path is omitted, the path is assumed to be `/` (the root). In order to parse the URL unambiguously, you must have a slash following the hostname or port number if you supply a query string or fragment identifier (discussed below).

### Query string: `?name=Shirley&gender=queer%20as%20fuck` (optional)

This is a query string encoding the following key-value pairs:

<table>
  <tr><th>key</th><th>value</th></tr>
  <tr><td>name</td><td>Shirley</td></tr>
  <tr><td>gender</td><td>queer as fuck</td></tr>
</table>

The key is associated with the value with an equals sign, and multiple values are strung together with equals signs. You may have noticed that the paces in `queer as fuck` have been replaced with the character sequence `%20`. This is called "percent encoding" or (intuitively enough) "URL encoding". Certain characters that are not welcome in URLs are replaced with equivalent sequences of `%##` (where `#` is a digit).

The query string is an odd beast. Your browser knows how to turn form inputs into query strings, sticking together multiple values and converting spaces to `%20`s with no trouble. However, the server on the receiving end may do something with the query string, or nothing at all. The path and query string come in to the server stuck together, and it's up to the server (perhaps even your program) to make sense of them.

### Fragment identifier: `#about-our-site` (optional)

Another odd one, but easier to explain. This one doesn't even get sent over the wire as part of the request. However, when using a web browser to load a document from a URL with a fragment identifier attached, the web browser will see if it matches up to an element in the page and jump to that section.

For example, you have a section on `http://example.com/animals` that begins with `<div id="cats">`. To allow users to skip right to the cats, you can link to http://example.com/animals#cats. The browser sees that there exists an element with an id of `cats` and jumps right to it. (This is used in tables of contents, for example those on Wikipedia.) As a special case, `#` links to the top of the page.

(Some people--who were too clever by half--decided to juggle query parameters around into fragment identifiers using JavaScript. That's why, for example, searching for "cats" on Google takes you to `https://www.google.com/#q=cats`. This has confused beginners greatly and I advise you to pretend I haven't mentioned it.)

## Methods (or verbs)

If HTTP only let you request a document and get the document in response, it would be plenty useful, but probably not give rise to the Web as we know it. Fortunately, HTTP also defines ways to send your own information up to the server.

Let's start with the simplest case: requesting a document using the `GET` method with a path derived from a URL.

### `GET`

When you type `google.com` into your browser's address bar and hit enter, what does the conversation between your browser and Google look like? The first thing the browser does (after figuring out that you meant `https://google.com/`) is fire off an HTTP `GET` request to `google.com` on port 443 (wrapping it in some encryption so nobody can snoop on your searches besides the NSA and Google). Incidentally, this is covered in incredible detail by [a collaboratively authored document on GitHub](https://github.com/alex/what-happens-when#what-happens-when). I'm going to elide some details.

We want to snoop on this conversation, so let's do it in the terminal instead of our browser. Use the `curl` utility with the `-v` (verbose) option to see happens.

```text
$ curl -v http://google.com/
*   Trying 2607:f8b0:4004:804::200e...
* TCP_NODELAY set
* Connected to google.com (2607:f8b0:4004:804::200e) port 80 (#0)
> GET / HTTP/1.1
> Host: google.com
> User-Agent: curl/7.51.0
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Location: http://www.google.com/
< Content-Type: text/html; charset=UTF-8
< Date: Sun, 04 Jun 2017 00:26:03 GMT
< Expires: Tue, 04 Jul 2017 00:26:03 GMT
< Cache-Control: public, max-age=2592000
< Server: gws
< Content-Length: 219
< X-XSS-Protection: 1; mode=block
< X-Frame-Options: SAMEORIGIN
<
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
* Curl_http_done: called premature == 0
* Connection #0 to host google.com left intact
```

Lines beginning with `*` describe what the cURL utility is doing under the hood to set up the connection. It converts `google.com` to an IP address (`2607:f8b0:4004:804::200e`), and there's that port 80 I keep mentioning.

The lines beginning with `> ` are the HTTP GET request your computer makes. The first line, `GET / HTTP/1.1`, says we want to retrieve the root document (`/`) over the HTTP/1.1 version of the protocol. cURL follows that up with some request headers that say which host we're trying to talk to (`Host: www.google.com`). Some servers have multiple hostnames answering to the same IP address, so it pays to be specific. The line with `User-Agent: curl/7.51.0` means that cURL identifies itself as the agent acting on our behalf. Chrome, Firefox, Safari, and others all advertise their origins in the `User-Agent` header, which is only really useful for statistics.

Finally, `Accept: */*` means cURL is willing to take any format that may be at that URL. If we wanted to be choosy, we could send `Accept: text/html` and express our preference for an HTML document in response.

In all but the latest version of HTTP, those are the exact characters (bytes) given to the network controller to send over the wire. (A more recent revision of the protocol, HTTP/2, makes certain changes for efficiency.)

The lines beginning with `< ` are the headers of the HTTP response from Google. After the lines with `< `, there is a very brief document, telling us we should have requested http://www.google.com/ instead.

Look closely at the first few lines of the response:

```text
< HTTP/1.1 301 Moved Permanently
< Location: http://www.google.com/
< Content-Type: text/html; charset=UTF-8
```

There's that `text/html` again. Even though we didn't specify it in `Accept:`, we got HTML back. Phew. The first line is interesting because it has a numeric code. This is an HTTP _status code_, the most famous of which is probably 404: File Not Found. The 301: Moved Permanently code is useful because it comes with the new location: `Location: http://www.google.com/`. Check out the [full list](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) if you're curious.

If we requested `http://www.google.com/` as instructed, we'd get the Google homepage. Try `curl -v http://www.google.com/` and see for yourself. The response is a bit longer, and not worth including here--especially as it's not a good example of how to format your documents!

### `POST`

The other commonly used HTTP method (or verb) is POST. As we will see later, web pages support fillable forms that submit their contents back to the server. When making such a submission will cause some important change on the server side, the form instructs the browser to use the `POST` method. This one is harder to snoop on, since we need an accomplice on the server side expecting a POST. (Trying to POST to a URL that isn't expecting it, like http://www.google.com/, will get you a 405: Not Allowed error.)

cURL knows how to craft a POST if we have some `key=value` pairs that look like form field names and values. To experiment, we can use https://httpbin.org. This service exposes some URLs specifically for testing and experimentation, including `http://httpbin.org/post` to spit back out anything `POST`ed to it.

Say we submit a form where we say our `goal` is to `website` good. This is how the transaction appears:

```text
$ curl -vF goal=website http://httpbin.org/post
*   Trying 23.21.145.230...
* TCP_NODELAY set
* Connected to httpbin.org (23.21.145.230) port 80 (#0)
> POST /post HTTP/1.1
> Host: httpbin.org
> User-Agent: curl/7.51.0
> Accept: */*
> Content-Length: 146
> Expect: 100-continue
> Content-Type: multipart/form-data; boundary=------------------------d6c693b8638da343
>
* Done waiting for 100-continue
< HTTP/1.1 100 Continue
< HTTP/1.1 200 OK
< Connection: keep-alive
< Server: meinheld/0.6.1
< Date: Sun, 04 Jun 2017 01:01:41 GMT
< Content-Type: application/json
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
< X-Powered-By: Flask
< X-Processed-Time: 0.00102806091309
< Content-Length: 459
< Via: 1.1 vegur
<
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "goal": "website"
  },
  "headers": {
    "Accept": "*/*",
    "Connection": "close",
    "Content-Length": "146",
    "Content-Type": "multipart/form-data; boundary=------------------------d6c693b8638da343",
    "Expect": "100-continue",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.51.0"
  },
  "json": null,
  "origin": "73.172.20.143",
  "url": "http://httpbin.org/post"
}
* Curl_http_done: called premature == 0
* Connection #0 to host httpbin.org left intact
```

Everything from the `{` to the `}` is a response from httpbin telling us what we stuck in. Sure enough, the `form` section says our goal is to website.

Armed with these basics, you're ready... to learn the other three underlying pillars of web applications! Ha, I bet you thought you were going to start writing Python or something.

# Languages for markup and presentation

You may note that we haven't actually started building our web application yet. That's because, in order to build any nontrivial web application, one must understand the web's protocols (which we just covered) as well as two or three languages that determine the appearance and behavior of the web pages you produce.

It bears mentioning that the educational background of Sir Tim Berners-Lee, creator of the World Wide Web, was in physics and not computer science. One might uncharitably interpret this as the source of the inelegance of the underlying languages and protocols. (One might charitably interpret this as the reason the web is actually _useful_ to people, rather than expressing achingly pure algorithms in perfect stasis where they won't accidentally cause side-effects.)

To build a webpage, you need Hypertext Markup Language (HTML). To make it pretty, you need Cascading Style Sheets (CSS). To add some kinds of interactivity, you need JavaScript (JS).

Together, these three horsepersons of the apocalypse form the so-called "HTML5 platform" or even just the "web platform". They're incredibly flexible, organically grown, and have been improved in fits and starts since 1989 (HTML) / 1994 (CSS) / 1996 (JS). Along the way, very smart people building the standards and web browsers across multiple companies have ironed out some kinks. However, in order to do so while preserving compatibility with older webpages, various warts and workarounds have built up over time.

The best resource on the web for all three languages is probably the [Mozilla Developer Network](https://developer.mozilla.org/). Mozilla is a non-profit organization that develops the Firefox browser (along with a number of other useful doodads). (Google may lead you to an outfit called W3Schools. They are a less reliable source. Use MDN.)

## Hypertext Markup Language (HTML)

Consider a very short and simple text document:

```
The Hubble Space Telescope is definitely bigger than me.
```

The defining characteristics of a _hypertext_ document are the capability for _hyperlinks_ and a _URL_. (The URL is really just the dual of the hyperlink: having a URL allows others to link to you.) If we want to convert our simple text document into a hypertext document, we need to give it a URL and add some hyperlinks. As we just discussed, this could be determined by a server's document root and a file path on disk. It could also be determined in our web application.

Hyperlinks are added to a document by use of HTML **tags**. The tag for a hyperlink is `<a>` (which stands for "link", of course 😝). Tag names are frequently written in angle brackets (as I just did), but in the wild they may have _attributes_ as well as a _closing_ or _end tag_.

### From text to HTML, just add hyperlinks... right?

Here's a hyperlinked version of the preceding document:

```
The <a href="http://hubblesite.org/">Hubble Space Telescope</a> is definitely bigger than me.
```

The `href="http://hubblesite.org/"` sets the `href` _attribute_ of the `<a>` tag to `http://hubblesite.org/`. Multiple attributes would be separated from each other by spaces, as in `<a href="http://hubblesite.org/" target="_blank">`.
  
The `</a>` is the _closing tag_. The first `<a>` tag (sometimes called the _opening_ tag) means "everything after this is part of a link". The closing tag says "okay, that's enough". If you forget a closing tag, your whole page turns into a link, and then where will you be?
  
Browsers are much more forgiving interpreters of HTML than, say, the Python interpreter would be of Python. You may screw up and the page will still look "okay", but other things are weird. Check that your tags are all closed, and note that "overlapping" tags are not allowed. For example, this is not legal:

```
<strong>This goes <a href="#">home</strong> or to the top</a>
```

Some browsers will compensate by moving the `</a>` inside the `</strong>` silently, but then do other weird things. Don't make browsers guess what you mean, and you'll both be happier. Communication is key to productive relationships of all kinds.

Now, our hyperlinked document about Hubble isn't quite complete as it stands. Go to the [W3C Markup Validation Service](http://validator.w3.org/#validate_by_input) and paste it into the "Validate by Direct Input" tab and you'll see a few cryptic sounding errors.

What they boil down to is this: We need to declare a document type. HTML comes in several different flavors, and we want to specify that we're using the latest and greatest. Stick `<!DOCTYPE html>` on the beginning like this:

```
<!DOCTYPE html>
The <a href="http://hubblesite.org/">Hubble Space Telescope</a> is definitely bigger than me.
```

Paste that into your validator. You should get some different errors. It turns out that we cannot have an HTML5 document without a `<title>`. Here's how that looks:

```
<!DOCTYPE html>
<title>About the Hubble</title>
The <a href="http://hubblesite.org/">Hubble Space Telescope</a> is definitely bigger than me.
```

The title must come before any content (besides the document type). The title you enter heredoesn't show up on the page, exactly. It's what comes up in search results before the content preview, or in the title bars of your tabs in your browser. Fix that, and revalidate. Should be all good now! Save these lines somewhere as `ex.html` and open that file up in a browser.

Verify that you can get to [HubbleSite](http://hubblesite.org) by clicking the link you just made. You can stick any URL in the `href` attribute of the `<a>` tag to change the target of the link. That's not quite the whole story. The URL we have in there, `http://hubblesite.org` is what is called an "absolute URL" (or sometimes "full URL"). It has all the pieces from before. However, there are good reasons you may not always wish to use the full URL.
  
### How else might you specify the target of a hyperlink?

Make a new document called `ex2.html` with these contents, and save it in the same folder as `ex.html`:

```
<!DOCTYPE html>
<title>Spare page</title>
Keep your extra bits here
```

Now, how can we link to `ex2.html`? We could specify the full `file:///` URL, but as mentioned previously, this won't work on someone else's computer--even if we gave them the files, their username is probably different from ours.

HTML supports URLs that omit some of the essential (non-optional!) pieces discussed before. Just as the port number can usually be inferred from the transport, other pieces of the URL can be inferred based on the context of where it appears. The user's browser does this all transparently.

#### URL with absolute path: Omit transport and hostname (and adjacent optional elements)

This is hard to illustrate without setting up a web server, so you'll have to take my word for it.

Suppose you put `ex.html` and `ex2.html` on the web at `http://www.example.com/mysite/ex.html` and `http://www.example.com/mysite/ex2.html`. When writing a link on `ex.html` to `ex2.html`, you could omit `http://www.example.com` as that's implied by the context. Your `href` attribute would then look like `href="/mysite/ex2.html"`.

#### URL with relative path: Omit transport, hostname, and partial path (and adjacent optional elements)

If you know the two documents are served from the same folder (or, for URLs served by a web application, are served from the same level in the path hierarchy), you don't even need the beginning of the path.

In the situation described above, your `href` attribute would then look like `href="ex2.html"`. This has the advantage of being independent of where you put the two files. In fact, try it now! You should be able to hyperlink from `ex.html` to `ex2.html` by changing the `href` attribute. Put that in your `ex.html` and save it.

### What is the true minimal HTML document?

That's just about the most minimal HTML document you can create, but all is not what it seems. There are a few implicit elements hiding here. To see what I mean, open up the developer tools for your browser. In Safari, this means opening Safari preferences, choosing the "Advanced" tab, and checking the box labeled "Show Develop menu in menu bar". Then, after you close the preferences window, choose "Show Web Inspector" from the "Develop" menu.

![Screenshot showing Safari web inspector]({attach}how-about-some-website/safari_web_inspector.png)

(As a brief aside, look at that wacky URL. It starts with `file:` and _three_ slashes if you're on a Mac or Linux. `file:///` URLs break some of the rules, but they are useful--albeit only for quick local testing, since other people can't see files on your computer!)

If you copy out the document as shown in the inspector, you'll get this:

```
<!DOCTYPE html>
<html>
<head>
  <title>About the Hubble</title>
</head>
<body>
  The <a href="http://hubblesite.org/">Hubble Space Telescope</a> is definitely bigger than me.
</body>
</html>
```

Where'd those extra elements come from? Well, it turns out they are there implicitly, whether you wrote them out or not. Arguably, this is useful when you're in a hurry or want to show a minimal example. When making a non-trivial web page, you'll probably want to start from something more like what your developer tools show.

It's time for the second horseperson: Cascading Style Sheets.

## Cascading Style Sheets

*To be written.*

## JavaScript

The third and final horseperson is JavaScript. "Modern" JavaScript is in a period of rapid evolution, with new tools and frameworks and libraries appearing by the week. The novice attempting to build website is likely better served by focusing on HTML and CSS first, adding JavaScript to the mix once familiarity with the former two has been achieved.

Perhaps a picture will be illustrative.

![JavaScript: The Good Parts is much smaller than JavaScript: The Definitive Guide]({attach}how-about-some-website/JavaScript-the-good-parts.jpg)

*Photo lifted from ["Why Mobile Web Apps are Slow"](http://sealedabstract.com/rants/why-mobile-web-apps-are-slow/) by Drew Crawford*

# Dynamic Websites and Web Applications

At the dawn of the World Wide Web, web server software was designed to serve resources from files on disk. A URL would point to an HTML document file, or a CSS file, or perhaps an image or other media. It didn't take too long for Computer People to realize that they could add value to documents by generating them on the fly when someone asked for them. Perhaps they could include the current date and time, in case the user forgot. Perhaps they could change the `src=` attribute on the `<img>` on the homepage to a new, random tasteful picture on each page load to confuse and disorient their users. Maybe include a weather report, customized for the user's location. (That one might actually be useful.)

The key development here is that a URL no longer had to be a file on disk, but rather could be an HTML document that was generated in memory, sent to the requester, and then discarded.

Because up until now, everything had to be achievable with boring old files on disk, dynamic websites gained (more or less by accident) a clean _separation of concerns_. The logic to generate the page content could be in any language, so long as it could spit out an HTML document in response to a user's request. Designers could work from a saved HTML document and test their changes on the associated CSS files without reloading the whole application. JavaScript developers... well, that wasn't a thing (yet).

We are going to construct a small example in [Flask](http://flask.pocoo.org) and Python 3.6. Flask is a library written in Python that abstracts away that `GET / HTTP/1.1` stuff into Python objects and calls functions you define with them.

## Responding to a GET from Python

## Templating

Back in the old days, web designers had trouble updating their fancy designs across an entire website. HTML documents are laid out more or less in source order (that is, elements that appear earlier in the HTML source code will be further up on the page). So, on a page with a header, a sidebar, and a footer, a "webmaster" would have to update every HTML file's beginning, end, and middle. Yikes.

(This may seem very intuitive, or it may not, but as a contrasting example: GUI libraries for most programming languages allow the layout of an application to be rearranged independent of the order in which components are defined in the source code.)

It didn't take long for web developers to realize that they could manage this complexity by building up pages on the fly. After all, there was no way that the browser could know (or care) that their HTML document was a franken-document made of `preamble.html` + `header.html` + `sidebar.html` + some content (perhaps retrieved from a database) + `footer.html`.

Then, if they wanted to update the appearance of the header, they only had to edit it in one place!

The grown-up version of this idea is called an "HTML template engine" or "HTML template library". It doesn't include the templates themselves, but rather defines a mini-language for composing reusable sections of HTML markup into final documents.

The template engine we are using is called [Jinja2](http://jinja.pocoo.org/), and it is bundled with Flask.

## Writing things Into The Internet™

Learn how to put a form in your website and get submitted values in your templates.

## Persistent buggers, aren't they?

How can you even persist things? Am I going to have to explain about databases? Ugh.

# Achieving maximum website through judicious reuse of free software

I hope I've convinced you that I am website and you can too.

The great thing about website is that people give you all kinds of junk for free. There are downsides to using the free website junk of others, of course. They may not have been very good at website, for example. Or, you may not understand the problem their free website junk solves, and end up using it wrong. Lastly, of course, your website will look and act like many others that used the same free website junk.

## Strap on your boots

The [Bootstrap library](http://getbootstrap.com) is one common way to make your website less hideous without spending too long on it. As we have discussed, websites are just text files with HTML, CSS, and JS combined in clever ways. Bootstrap provides CSS and JS, as well as some suggested arrangements of HTML elements (with certain class names or IDs) that play well with their stylesheets.

## WTForms

As Flask is a so-called "microframework", it leaves much up to the developer. This could be bad. For example, what if you don't know what you're doing? You might do it wrong.

One of the absolute worst things about making website is that people keep trying to exploit them. Just terrible. They write malicious things into the Internet, and then they steal your grandparents' credit card numbers. You must be ever vigilant against User Input.

This is good practice for all programming. What the hell does the user know, anyway? They're probably totally drunk right now.

WTForms lets you define some form classes which you can then use to validate (sanity-check) the input of your wily users. Keep them from putting bad stuff into website.

## The wonderful world of databases

They will solve all your problems but also create more problems have fun okay bye.