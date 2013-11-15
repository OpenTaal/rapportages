#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from difflib import SequenceMatcher

def row(report_file, id, next, word, sentences, corrections):
    corrs = ''
    words = ''
    first = True
    for cor in corrections:
        word_layout = []
        word_index = -1
        correction_layout = []
        correction_index = -1
        s = SequenceMatcher(None, word, cor)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
#            print ("%7s word[%d:%d] (%s) cor[%d:%d] (%s)" %(tag, i1, i2, word[i1:i2], j1, j2, cor[j1:j2]))
            if tag == 'delete':
                if word_index == -1:
                    word_layout.append(word[:i1])
                word_layout.append('<span style="background-color:#ff8888;">%s</span>' %word[i1:i2])
                word_index = i2
            elif tag == 'replace':
                word_layout.append('<span style="background-color:#ffcc88;">%s</span>' %word[i1:i2])
                word_index = i2
                correction_layout.append('<span style="background-color:#88ffcc;">%s</span>' %cor[j1:j2])
                correction_index = j2
            elif tag == 'equal':
                word_layout.append(word[i1:i2])
                word_index = i2
                correction_layout.append(cor[j1:j2])
                correction_index = j2
            elif tag == 'insert':
                correction_layout.append('<span style="background-color:#88ff88;">%s</span>' %cor[j1:j2])
                correction_index = j2
        if word_index == -1:
            word_layout = word
        else:
            word_layout = ''.join(word_layout)
        if correction_index == -1:
            correction_layout = cor
        else:
            correction_layout = ''.join(correction_layout)
        if first:
            first = False
            words += word_layout
            corrs += correction_layout
        else:
            words += '<br>' + word_layout
            corrs += '<br>' + correction_layout
    if next == 'X':
        next = '<strong>X</strong>'
#    if link:
#        if first:
#            report_file.write('<tr><td><a target="_blank" href="http://data.opentaal.org/opentaalbank/spellingcontrole/next_version/bewerkWoordenlijst.php?wordfilter=^%s%%24">%s</a>&nbsp;</td><td>%s</td><td><a target="_blank" href="http://data.opentaal.org/opentaalbank/woorddetails.php?word=%s">i</a>&nbsp;</td><td>%s</td><td><a target="_blank" href="http://data.opentaal.org/opentaalbank/woorddetails.php?word=%s">i</a>&nbsp;</td><td>&nbsp;%1.2f</td></tr>\n' %(word, next, word_layout, word, correction_layout, correction, s.ratio()))
#        else:
#            report_file.write(u'<tr><td>&nbsp;</td><td>%s</td><td>↲&nbsp;</td><td>%s</td><td><a target="_blank" href="http://data.opentaal.org/opentaalbank/woorddetails.php?word=%s">i</a>&nbsp;</td><td>&nbsp;%1.2f</td></tr>\n' %(word_layout, correction_layout, correction, s.ratio()))
#    else:
#        if first:
#            report_file.write('<tr><td>%s&nbsp;</td><td>%s</td><td><a target="_blank" href="http://data.opentaal.org/opentaalbank/woorddetails.php?word=%s">i</a>&nbsp;</td><td>%s</td></tr>\n' %(next, word_layout, word, correction_layout))
#        else:
#            report_file.write('<tr><td>&nbsp;</td><td>%s</td><td></td><td>%s</td></tr>\n' %(word_layout, correction_layout))
    report_file.write('<tr><td>%s</td><td>%s</td><td><a target="_blank" href="http://data.opentaal.org/opentaalbank/woorddetails.php?word=%s">%s</a></td><td>%s</td><td>%s</td></tr>\n' %(id, next, word, sentences, words, corrs))

def report(link=False):
    name = 'rapportage-fouten-met-correcties'
    if link:
        name += '-en-links'
    report_file = codecs.open('correcties.html', 'w', 'utf-8')
    report_file.write(u"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rapportage foute woorden met correcties</title>
<link rel="stylesheet"  href="jquery.mobile-1.3.2.min.css">
<link rel="shortcut icon" href="images/opentaal.png">
<script src="jquery-1.10.2.min.js"></script>
<script src="jquery.mobile-1.3.2.min.js"></script>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
</head>
<!--body style="font-family:courier;"-->
<body> 
<div data-role="page">

        <!-- default panel  -->
        <div data-role="panel" id="defaultpanel">
<h3>Legenda</h3>
<p>OpenTaal heeft meer dan 12.000 foute woorden in haar collectie. Van meer dan 10% zijn ook correcties opgenomen. Deze worden hier getoond om herzien te kunnen worden. Deze correcties zijn noodzakelijk om de suggesties van de automatische spellingcontrole te kunnen valideren. Inmiddels hebben we 700 uitzonderingen voor de spellingcontrole die bijvoorbeeld de volgorde van de suggesties verbetert of suggesties toevoegt die niet werden aangeboden. Onderstaande fouten en correcties zijn dus belangrijk voor een betere spellingcontrole met een groter gebruikersgemak.</p>
<table border="1">
<tr><th></th><th>betekenis</th><tr>
<tr><td><strong>X</strong></td><td>woord is gemarkeerd als fout</td><tr>
<tr><td>x</td><td>woord is gepland om als fout te markeren</td><tr>
<tr><td><span style="background-color:#ff8888;">&nbsp;&nbsp;</span></td><td>letters die verwijderd moeten worden</td><tr>
<tr><td><span style="background-color:#ffcc88;">&nbsp;&nbsp;</span></td><td>letters die vervangen moeten worden</td><tr>
<tr><td>i</td><td>link naar voorbeeldzinnen met foute woord</td><tr>
<tr><td><span style="background-color:#88ff88;">&nbsp;&nbsp;</span></td><td>letters die toegevoegd worden</td><tr>
<tr><td><span style="background-color:#88ffcc;">&nbsp;&nbsp;</span></td><td>letters die voor vervanging zorgen</td><tr>
</table>
<p>Soms heeft een fout woord meerdere correcties. Dit is te herkennen bij de extra correcties die geen <strong>X</strong> of x in de eerste kolom hebben. Meerdere correcties lopen af in relevantie. Het liefst is er maar een enkele correctie per fout woord opgegeven. Dat is niet altijd mogelijk maar er wordt gestreefd naar een correctie per fout woord.</p>
<p>Lees nevenstaande lijst door en laat ons weten wat verbeterd kan worden via <a href="mailto:info@opentaal.org?subject=Correctie fout woord">info@opentaal.org</a>.</p>
        <a href="#demo-links" data-rel="close" data-role="button" data-theme="c" data-icon="delete" data-inline="true">Sluit paneel</a>
        </div><!-- /default panel -->

<div data-role="content" class="jqm-content">
<a href="#defaultpanel" data-role="button" data-inline="true" data-icon="bars" data-theme="b">Rapportage foute woorden met correcties</a>
""")

    report_file.write("""<table data-role="table" id="table-column-toggle" data-mode="columntoggle" class="ui-responsive table-stroke" data-column-btn-text="Kolommen" data-column-btn-theme="b">
     <thead>
       <tr>
         <th data-priority="5">ID</th>
         <th data-priority="3">Status</th>
         <th data-priority="1"><abbr title="Zinnen waarin">Zinnen</abbr></th>
         <th>Woord</th>
         <th>Correctie</th>
       </tr>
     </thead>
     <tbody>
""")
#    if link:
#        report_file.write('<tr><th colspan="3">woord</th><th colspan="2">verbetering</th><th>ratio</th></tr>\n')
#    else:
#        report_file.write('<tr><th colspan="3">woord</th><th>verbetering</th></tr>\n')
    all_words = []
    all_corrections = []
    for line in codecs.open('fouten-met-correcties.tsv', 'r', 'utf-8'):
        line = line.strip()
        if line.count('\t') < 4:
            print 'ERROR:', line
            exit(1)
        (id, next, word, sentences, corrections) = line.split('\t')
        if word not in all_words:
            all_words.append(word)
        corrs = []
        if ';' in corrections:
            corrs = corrections.split(';')
        else:
            corrs.append(corrections)
        for corr in corrs:
            if corr not in all_corrections:
                all_corrections.append(corr)
        row(report_file, id, next, word, sentences, corrs)
#    if link:
#        report_file.write('<tr><th colspan="3">woord</th><th colspan="2">verbetering</th><th>ratio</th></tr>\n')
#    else:
#        report_file.write('<tr><th colspan="3">woord</th><th>verbetering</th></tr>\n')
    report_file.write('</tbody></table>\n')
    report_file.write("""</div>
</div>
</body>
</html>""")
    
    for word in all_words:
        if word in all_corrections:
            print 'ERROR: gebruikt als fout woord en als correctie: %s' %word
    
report()
#report(True)
