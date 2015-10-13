Title: Why does reading data from a file-like object "consume" it?
Date: 2015-04-13
Slug: file-like-objects-in-python
Summary: Sometimes, one tries to iterate over some content more than once, and Python acts like it only iterated once. Here's the reason why, and some historical context for it.

In a recent class, the instructor showed some example code that iterated over a response from a web service, printing it out. The next exercise was to do something other than printing with that same data, but the students were surprised to find that iterating over the same response object again didn't seem to do anything. This is my attempt to explain what was going on.

Consider this code:

    import urllib
    response = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=AAPL,MSFT,GOOG&f=sl1")
    for line in response:
        print line,

This prints out:

    "AAPL",128.05
    "MSFT",41.88
    "GOOG",541.80

What if you wanted to see the output twice? The quick and dirty way seems to be copying and pasting the loop a second time:

    import urllib
    response = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=AAPL,MSFT,GOOG&f=sl1")
    for line in response:
        print line,
    for line in response:
        print line,

This prints out:

    "AAPL",128.05
    "MSFT",41.88
    "GOOG",541.80

## Wait, what?

Why didn't it print out our stock prices twice?

The answer has to do with the fact that `response` is not a list or tuple, even though we're using `for line in response` to iterate over it. Just to check, let's see what happens if we make `response` into a list before we iterate. Below, we've added `list()` around the call to `urlopen`.

    import urllib
    response = list(urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=AAPL,MSFT,GOOG&f=sl1"))
    for line in response:
        print line,
    for line in response:
        print line,

Et voila!

    "AAPL",128.05
    "MSFT",41.88
    "GOOG",541.80
    "AAPL",128.05
    "MSFT",41.88
    "GOOG",541.80

## So, if it's not a list, what kind of thing is `response`?

The `response` object returned by `urlopen` is what is called a "file-like object" in Python. (You may also see them called "file objects" or "streams".) This means that it has certain methods and behaviors that are analogous to the file objects you get from calling, e.g. `open('myfile.dat', 'r')`.

Handling data from files is somewhat different from handling variables in memory (like a list you defined in your program). When figuring out how programmers should interact with files in Python, the language designers wanted to make sure that programmers could work with files much larger than the available system memory.

## Consider a huge file...

Say you have a 1 TB file called `my_large_file.dat`, and you open it as `f`:

    f = open('my_large_file.dat', 'r')

Now, our computer only has 10 GB of RAM, so what's happening with `f`? It's not all 1000 GB of data from `my_large_file.dat`, because that would make us run out of memory. It's a "file object", sometimes called a "file handle". It lets you manipulate the file on disk without reading in the whole thing. This lets us process files much larger than our system memory by reading in a little chunk of the file, doing something to that chunk, and then moving on to the next.

Before, we were using `for line in ...` to process a line at a time, but the lower-level (that is, more explicit) way to read data from a file is to use `f.read()`. The `f.read()` method takes a number as its first argument, which tells the file object how many bytes you want. For example, to read one byte from `f`, you'd do `f.read(1)`. (It counts in bytes because the file object doesn't know about lines, at this level.)

When we first open `f`, it has a "current position" of 0, meaning the next `f.read()` will start counting from the beginning.

We're going to read 1024 bytes (1 kilobyte) at a time, using `f.read(1024)`. Below is a diagram of how Python thinks about your big file, right after you call `open()`:

    [    first 1k chunk    ][    second 1k chunk    ][ ...
    ^
    current position

We read 1024 bytes with `first_chunk = f.read(1024)`. Now the Python picture looks like this:


    [    first 1k chunk    ][    second 1k chunk    ][ ...
                            ^
                     current position


Next, we do `second_chunk = f.read(1024)`. The function call `f.read(1024)` looks exactly the same, but the file object remembers its current position from last time. The next 1024 bytes we request come from that position, already 1024 bytes into the file.

## What happens when we get to the end?

Suppose we've gone through the whole 1 TB file, 1024 bytes at a time, and we're nearing the end. We have one chunk left.

    ... ][    last 1k chunk    ]
         ^
    current position

We do `last_chunk = f.read(1024)`. This reads the last 1024 bytes in, and moves the "current position" that the `f` object keeps track of to the end. Now the picture looks like this.

    ... ][    last 1k chunk    ]
                               ^
                        current position

What happens if we try to read beyond the end of the file? It's not clear what *should* happen. Should we start over from the beginning? Should we start reading the next file on disk? Should we raise an exception? There are cases where you might want any of these behaviors, or something else entirely.

Python's language designers (following the example of other, older languages) decided [this](https://docs.python.org/2/tutorial/inputoutput.html#methods-of-file-objects) should be the behavior:

> To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string. size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size bytes are read and returned. **If the end of the file has been reached, f.read() will return an empty string ("").**

That may not *always* be what you want, but it is *consistent*. Any time you have a file-like object (unless someone has specified otherwise), you'll get this behavior.

This is what was happening up above where we tried to loop with `for line in response` twice. The end of the "file" (really, the response from the website) had been reached. When we tried to loop over it again, the `response` object looked at the "current position" it was tracking, concluded there was nothing left, and **happily looped zero times.**

## But how is `urlopen` anything like reading a file?

Well, firstly, by analogy with `open()`, the name implies it'll behave similarly. That's not much help if you didn't already know that subtlety of file objects, but there you go.

Secondly, from the perspective of a language designer, "getting things from disk" and "getting things from the Web" are pretty similar. They both involve getting data from "elsewhere" (broadly defined) and reading it into a temporary buffer a bit at a time.

File handling on computers has inherited a lot of functionality from how computers worked historically. For example, file objects in Python have a `seek()` method that takes a position. This comes from the days of tape and old, rotating hard drives. In those days, to read a file in any order besides "first byte, then second, then third, and so on", you would have to tell your drive to "seek" a new position. Just like fast-forwarding or rewinding a tape.

File objects in Python keep track of a "current position" internally because computers used to have to keep track of a tape head or rotating drive head in order to know where the next data were coming from. Even though today you'll only need this when working on files bigger than your available RAM, and the task of moving a drive head has been delegated to the operating system, a lot of programming languages still use these semantics for files. (Not just Python!)

## But we were using `for line in response`, not `response.read()`...

Right! Python lets things other than lists, tuples, and dicts "hook in" so that you can iterate over them with `for blah in ...`. Behind the scenes, Python is following a process like "do `foo = response.read()`, look for a line separator in `foo`, send everything up to the line separator to the loop, hold on until the next step".

When the "current position" marker for `response` gets to the end, that process gets an empty string, sees no line separator, and decides that the loop is over.

This is just one example of an **iterator**. In Python, an iterator is any object that knows how to hook in to `for` loops and other forms of iteration. An iterator is a more general concept than a sequence or container type (like list, tuple, dict, and set). The only things required for a Python object to hook in to `for` loops are a `__iter__` method returning `self` and a `next` method (called `__next__` in Python 3.x) returning the next item in the sequence or raising the `StopIteration` exception. It is important to note what is **not** required: namely, there's no requirement that the iterator remember anything about the previous steps, or indeed know *anything* but the very next step it is to return.

We already saw how this makes for a nice abstraction around a file: Python does the bookkeeping behind the scenes and makes it look like you have a list of lines you're looping over. Other cases you might see a "consumable" (or "one-shot") iterator include retrieving results from a database query, or working with a generator expression (a subtle but useful topic in its own right).