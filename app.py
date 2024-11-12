from flask import Flask, render_template, redirect, url_for
import pandas as pd
from charts.charts import bar_chart, bar_chart_with_special_legend, point_chart, pie_chart

app = Flask(__name__)

# Read the CSV file

def translate_csv(file, translation_dict):
    with open(file, 'r') as f:
        text = f.read()
    for key, value in translation_dict.items():
        text = text.replace(key, value)
    with open('data/umfrage2survey.csv', 'w') as f:
        f.write(text)

translation_dict = {
    'Wie sind Sie auf WissKI aufmerksam geworden?': 'How did you hear about WissKI?',
    'In welchem Bereich verwenden Sie WissKI?': 'In which area do you use WissKI?',
    'Wie lange arbeiten Sie mit WissKI?': 'How long do you work with WissKI?',
    'Bedeutung von Softwarefeatures und Eigenschaften': 'Importance of software features and properties',
    'In welcher Rolle benutzen Sie WissKI?': 'In which role do you use WissKI?',
    'Haben Sie Erfahrung mit anderen Forschungsdaten-Management-Systemen?': 'Do you have experience with other research data management systems?',
    'Haben Sie Zugriff auf kompetenten IT- und Systemadministrationssupport innerhalb Ihres Projektes bzw. Institution?': 'Do you have access to competent IT and system administration support within your project or institution?',
    'Arbeitet Ihre Institution/ Unternehmen das erste Mal mit WissKI?': 'Is this the first time your institution/company has worked with WissKI?',
    'Wie viele Stunden stehen Ihnen für die Arbeit mit WissKI wöchentlich zur Verfügung?': 'How many hours a week do you have available for working with WissKI?',
    'Welchen Community-Angeboten haben Sie mindestens einmal wahrgenommen?': 'Which community offers have you used at least once?',
    'Im Verhältnis zu anderen Forschungsdaten-Management-Systemen verorte ich die Qualität von WissKI als...': 'In relation to other research data management systems, I classify the quality of WissKI as...',
    'Wie wahrscheinlich ist es, dass Sie WissKI als Forschungsdaten-Management-System weiterempfehlen?':'How likely is it that you would recommend WissKI as a research data management system?',
    'Kolleg:innen/ Bekannte':'Colleagues/ friends',
    'Studium':'Studies',
    'Ergebnis einer Online-Suchmaschine':'Result of an online search engine',
    'Vortrag/Poster':'Presentation/ Poster',
    'Erwähnt in einem Forschungsartikel':'(Research) Article',
    'Verwendung in einem Projekt':'Usage in a project',
    'Museum oder Sammlung':'Museum or collection',
    'Geisteswissenschaftliche Projekte': 'Humanity projects',
    'Archivwesen':'Archive',
    'Bibliothekswesen':'Library',
    'Provenienzforschung':'Provenance',
    'Architekturgeschichte':'Architecture',
    'Kunstgeschichte':'Art history',
    '3D-Rekonstruktion':'3D',
    'Regionalwissenschaften':'Area studies',
    'Unter einem Jahr':'Less than one year',
    'Ein bis drei Jahre':'One to three years',
    'Zwischen drei bis zehn Jahre':'Between three and ten years',
    'Über zehn Jahre':'More than ten years',
    'Weiß nicht/ keine Angabe':'I don\'t know/ no answer',
    'Eine gefühte Installation':'A guided installation',
    'Eine breite Medienintegration':'Broad media integration',
    'Die Einrichtung von Schnittstellen (REST, SPARQL)':'Setting up interfaces (REST, SPARQL)',
    'Die Integration von Normdaten (Geonames, GND...)':'The integration of standardised data (Geonames, GND...)',
    'Semantische Datenmodellierung (Ontologie-Anbindung)':'Semantic data modelling (ontology connection)',
    'Breite Import- und Export-Möglichkeiten':'Wide range of import and export options',
    'Flexible Dateneingabe und Darstellungsmöglichkeiten':'Flexible data input and display options',
    'Erweitere Konfiguration der Suche':'Extended configuration of the search',
    'Performance & Skalierbarkeit (Datenmengen > 10 000 Entitäten)':'Performance & scalability (data volumes > 10,000 entities)',
    'Vorhandensein von Vorlagen und Templates':'Vorhandensein von Vorlagen und Templates',
    'Design & Layoutanpassung':'Design & layout customisation',
    'Kollobatives Arbeiten':'Collobative working',
    'Freie Software (keine Lizenzkosten)':'Free software (no licence costs)',
    'Open Source (Quellcode selbstständig anpassbar) ':'Open source (source code can be customised independently)',
    'Sitebuilder*in (Seiten, Views, Suche und Inhalte erstellen, rudimentäre Layout-Anpassungen)':'Sitebuilder (create pages, views, search and content, rudimentary layout customisations)',
    'Datenmodellierer*in (Ontology-Engineering, Pathbuilder, Feldkonfiguraton unter WissKI Entities and Bundles)':'Data modeling (Ontology-Engineering, Pathbuilder, Feldkonfiguraton unter WissKI Entities and Bundles)g',
    'System- und Serveradministrator*in (evtl. Containervirtualisierung)':'System and server administrator (possibly container virtualisation)',
    'Redakteur*in bzw. Autor*in (ausschließlich Dateneingabe oder Korrektur)':'Editor or author (data entry or correction only)',
    'Entwickler*in (Programmierung und Quellcode-Anpassung und -Erweiterung)':'Developer (programming and source code customisation and extension)',
    '(UX-) Designer*in (benutzerdefinierte Layout-Anpassung)':'(UX) Designer (custom layout customisation)',
    'Projektmanager*in (Koordination, Konzeption und Leitung)':'Project manager (coordination, conception and management)',
    'Ja':'Yes',
    'Nein':'No',
    'Weiß nicht':'Don\'t know',
    'No, es gab Vorgängerprojekte/ gibt parallele Projekte':'No, there were predecessor projects/ there are parallel projects',
    'Bis 8':'up to 8',
    '8 bis 20':'8 to 20',
    '20 bis 30':'20 to 30',
    'Über 30':'Over 30',
    'Ich besuche die News-Sektion von wiss-ki.eu.':'I visit the news section of wiss-ki.eu.',
    'Ich folge WissKI auf https://fedihum.org/@wisski.':'I follow WissKI on https://fedihum.org/@wisski.',
    'Ich bin aktiv auf chat.wiss-ki.eu.':'I am active on chat.wiss-ki.eu.',
    'Ich nehme an den weeklies oder quaterlies auf wiss-ki.eu/weekly teil.':'I take part in the weeklies wiss-ki.eu/weekly or quaterlies on wiss-ki.eu/quaterly',
    'Ich nehme an den WissKI Anwender:innentreffen teil.':'I take part in the WissKI user meetings.',
    'Ich pflege informellen Kontakt mit anderen WissKI-Anwender*innen oder Entwickler*innen.':'I maintain informal contact with other WissKI users or developers.',
    'Ich folge WissKI auf https://www.drupal.org/project/wisski.':'I follow WissKI on https://www.drupal.org/project/wisski.',
    'Ich folge WissKI auf https://git.drupalcode.org/project/wisski.':'I follow WissKI on https://git.drupalcode.org/project/wisski.',
    'Ich besuche https://www.arthistoricum.net/netzwerke/wisski':'I visit https://www.arthistoricum.net/netzwerke/wisski',
    'Weit über dem Durchschnitt': 'Far above average',
    'Etwas unter dem Durchschnitt': 'Somewhat below average',
    'Im Durchschnitt': 'Average',
    'Weit unter dem Durchschnitt': 'Far below average',
    'Etwas über dem Durchschnitt': 'Somewhat above average',
    'Weit über dem Durschnitt': 'Far above average',
    'Etwas unter dem Durschnitt': 'Somewhat below average',
    'Im Durschnitt': 'Average',
    'Weit unter dem Durschnitt': 'Far below average',
    'Etwas über dem Durschnitt': 'Somewhat above average',
    'Kann ich nicht beurteilen/ keine Angabe': 'Can\'t judge/ no information',
}

translate_csv('data/Community-Umfrage.csv', translation_dict)

df = pd.read_csv('data/umfrage2survey.csv', encoding='utf8')
#df = pd.read_csv('data/Community-Umfrage.csv', encoding='utf8')

plots = {}

# Normal bar charts
# 1 Wie sind Sie auf WissKI aufmerksam geworden?
# 2 In welchem Bereich verwenden Sie WissKI?
# 25 Haben Sie Zugriff auf kompetenten IT- und Systemadministrationssupport innerhalb Ihres Projektes bzw. Institution?
# 26 Arbeitet Ihre Institution/ Unternehmen das erste Mal mit WissKI?

bar_charts = [1,2,25,26]
for chart in bar_charts:
  question_data = df.iloc[:, chart]
  question_plot = bar_chart(question_data, question_data.name)
  plots[chart] = (question_data.name, question_plot)

# Cleaned pie charts
# 23 In welcher Rolle benutzen Sie WissKI?
question_data = df.iloc[:, 23]
for index, value in question_data.items():
    new_value = value.split(' (')[0]
    question_data[index] = new_value

question_plot = pie_chart(question_data, question_data.name)
plots[3] = (question_data.name, question_plot)

# Normal Pie charts
# 3 Wie lange arbeiten Sie mit WissKI?
# 24 Haben Sie Erfahrung mit anderen Forschungsdaten-Management-Systemen?
# 27 Wie viele Stunden stehen Ihnen für die Arbeit mit WissKI wöchentlich zur Verfügung?
# 28 Welchen Community-Angeboten haben Sie mindestens einmal wahrgenommen?
pie_charts = [3,24,27,28]
for chart in pie_charts:
  question_data = df.iloc[:, chart]
  question_plot = pie_chart(question_data, question_data.name)
  plots[chart] = (question_data.name, question_plot)

# Point charts
# 9-22 Software Features
median_values = df.iloc[:, 9:23].median()
median_values_cleaned = pd.Series(name='Software Features')
for index, value in median_values.items():
    new_index = index.split(' [')[1].split(']')[0]
    median_values_cleaned[new_index] = value

point_plot = point_chart(median_values_cleaned, 'Software Features')
plots[9] = ('Software Features', point_plot)


# Bar charts with median
# 29 Im Verhältnis zu anderen Forschungsdaten-Management-Systemen verorte ich die Qualität von WissKI als...
bar_charts_with_median = [29]
for chart in bar_charts_with_median:
  question_data = df.iloc[:, chart]
  question_plot = bar_chart_with_special_legend(question_data, question_data.name, 'quality')
  plots[chart] = (question_data.name, question_plot)

bar_charts_with_median = [31]
for chart in bar_charts_with_median:
  question_data = df.iloc[:, chart]
  question_plot = bar_chart_with_special_legend(question_data, question_data.name, 'recommendation')
  plots[chart] = (question_data.name, question_plot)

plots = dict(sorted(plots.items(), key=lambda x: x[0]))

# Generate list of charts
charts = [{'id': i+1, 'title': plots[col][0], 'data': plots[col][1]} for i, col in enumerate(plots.keys())]

@app.route('/')
def index():
    return redirect(url_for('show_chart', chart_id=1))

@app.route('/chart/<int:chart_id>')
def show_chart(chart_id):
    chart = next((c for c in charts if c['id'] == chart_id), None)
    if not chart:
        return redirect(url_for('index'))

    plot_url = chart['data']
    prev_id = chart_id - 1 if chart_id > 1 else len(charts)
    next_id = chart_id + 1 if chart_id < len(charts) else 1

    return render_template('chart.html', plot_url=plot_url, prev_id=prev_id, next_id=next_id, title=chart['title'])

if __name__ == '__main__':
    app.run(debug=True)
