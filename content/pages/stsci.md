Title: Joseph Long at STScI
Slug: stsci
HTML: true

<style type="text/css">
#stsci-headshot {
    float: left;
    width: 7em;
    margin: 1em;
}
.headings h1, .headings h2 {
    text-align: left;
}
#post-header .headings h1#post-title {
    margin-top: 0.75em;
}
.headings {
    overflow: hidden;
}
#skills {
    font-size: 0.85em;
    width: 100%;
}
#skills td {
    vertical-align: top;
}
#skills ul {
    list-style-type: none;
}
#skills li {
    margin: 0.25em 0;
    padding: 0.5em;
    position: relative;
}

li.level1:before, li.level2:before, li.level3:before {
    content: '\2B24';
    font-size: 12px;
    display: inline-block;
    position: absolute;
    left: -1em;
    top: 0.4em;
}

li.level1:before {
    color: #15D600;
}

li.level2:before {
    color: #F0C413;
}
li.level3:before {
    color: #ccc;
}
.mobile-only {
    display: none;
}


@media screen and (max-width: 768px) {
    .mobile-only {
        display: block;
    }
    .full-only {
        display: none;
    }
    #skills td {
        display: block;
    }
    li.level1:before, li.level2:before, li.level3:before {
        content: '\25C9';
        top: 0.46em;
    }
    #post-header .headings h1#post-title {
        margin-top: 0.75em;
        font-size: 1.5em;
    }
}

</style>
<header id="post-header" class="block">
  <div class="headings">
    <img src="/css/stsci_headshot.png" alt="Headshot taken at STScI" id="stsci-headshot">
    <h1 id="post-title">Joseph Long @ STScI</h1>
    <h2>Research &amp; Instrument Analyst</h2>
  </div>
</header>
<section class="block">
    <h2>What I&rsquo;m doing</h2>
    <ul>
       <li>Working in the INS/TEL (Telescopes) group on JWST and AFTA/WFIRST</li>
       <li>Enhancing WebbPSF, Marshall Perrin's Webb point-spread function calculator, with new functionality</li>
       <li>Enhancing POPPY, the general use Fraunhofer optics simulation package (and companion to WebbPSF)</li>
       <li>Creating WFIRSTPSF, a tool like WebbPSF for use with the WFIRST mission</li>
   </ul>
</section>
<section class="block">
    <h2>Technical Skills</h2>
<table id="skills">
    <tr class="full-only">
        <th>Analysis</th>
        <th>Programming</th>
        <th>Communication</th>
    </tr>
    <tr>
        <td>
            <h2 class="mobile-only">Analysis</h2>
            <ul>
                <li class="level1">Proficient with AstroPy</li>
                <li class="level1">Proficient with PyRAF</li>
                <li class="level1">Proficient with non-interactive PyRAF use (pipeline-assembly)</li>
                <li class="level2">Familiar with creating new PyRAF packages</li>
                <li class="level2">Familiar with periodicity analysis (<a href="https://www.univie.ac.at/tops/Period04/" target="_blank">Period04</a>, <a href="http://exoplanetarchive.ipac.caltech.edu/cgi-bin/Periodogram/nph-simpleupload" target="_blank">Exoplanet Archive periodogram tool</a>)</li>
                <li class="level2">Familiar with Mathematica</li>
                <li class="level2">Familiar with IDL</li>
            </ul>
        </td>
        <td>
            <h2 class="mobile-only">Programming</h2>
            <ul>
                <li class="level1">Proficient with Python</li>
                <li class="level1">Proficient with <a href="http://scipy.org" target="_blank">Scientific Python</a> (NumPy, SciPy, matplotlib, etc.)</li>
                <li class="level1">Proficient with UNIX concepts (incl. basic shell scripting)</li>
                <li class="level1">Proficient with relational databases (MySQL, PostgreSQL)</li>
                <li class="level1">Proficient with HTML and CSS</li>
                <li class="level2">Familiar with JavaScript</li>
                <li class="level3">Learning C</li>
            </ul>
        </td>
        <td>
            <h2 class="mobile-only">Communication</h2>
            <ul>
                <li class="level1">Proficient with presenting analysis through <a href="http://ipython.org/notebook.html" target="_blank">IPython notebooks</a></li>
                <li class="level1">Proficient with graphic design for web and print</li>
                <li class="level2">Familiar with web-based data visualization library <a href="http://d3js.org" target="_blank">d3.js</a></li>
                <li class="level3">Blogging on the side at <a href="http://joseph-long.com/writing/" target="_blank">joseph-long.com/writing</a></li>
            </ul>
        </td>
    </tr>
</table>
</section>