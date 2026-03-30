---
permalink: /
title: "Background"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<div class="academic-home" markdown="1">

I am a Ph.D. student in Computer Science at Clemson University. My research focuses on 3D computer vision, trustworthy AI, and robust perception for autonomous driving systems.

Before Clemson, I received an M.S. in Electrical and Computer Engineering from Carnegie Mellon University and a B.S. in Computer & Systems Engineering from Rensselaer Polytechnic Institute.

<p class="academic-home__links"><a href="/files/CV_RW.pdf">CV (PDF)</a> | <a href="https://scholar.google.com/citations?user=lYRE8BgAAAAJ&hl=en">Google Scholar</a> | <a href="https://github.com/RunWang123">GitHub</a> | <a href="mailto:runw@clemson.edu">Email</a></p>

## Research Topics
* 3D Vision
* AI Security
* Mobile Computing

## Selected Publications
{% assign featured_pubs = site.data.publications.publications | where: "featured", true | sort: "date" | reverse %}
{% for pub in featured_pubs limit: 5 %}
* **{{ pub.title }}**. {{ pub.authors }}. {{ pub.venue_short | default: pub.venue }}, {{ pub.year }}{% if pub.acceptance_rate and pub.acceptance_rate != "" %} (Acceptance Rate: {{ pub.acceptance_rate }}){% endif %}{% if pub.url and pub.url != "" %}. [Link]({{ pub.url }}){% endif %}
{% endfor %}

## Research Experience Snapshot
{% assign research_items = site.data.cv.research | sort: "startDate" | reverse %}
{% for item in research_items limit: 3 %}
* **{{ item.position }}**, {{ item.company }} ({{ item.startDate }}{% if item.endDate %} – {{ item.endDate }}{% endif %})
{% endfor %}

## Recent Highlights
{% assign highlights = site.data.highlights.highlights | sort: "timestamp" | reverse %}
{% for highlight in highlights limit: 8 %}
{% if highlight.type == "news" %}
* [{{ highlight.timestamp | date: "%m/%d/%Y" }}] {{ highlight.title }}{% if highlight.description != "" %} ({{ highlight.description }}){% endif %}
{% elsif highlight.type == "publication" %}
{% assign publications = site.data.publications.publications %}
{% for pub in publications %}
{% if pub.id == highlight.publication_id %}
{% unless pub.status == "preprint" or pub.venue_short == "arXiv" or pub.note == "arXiv preprint" %}
* [{{ highlight.timestamp | date: "%m/%d/%Y" }}] **{{ pub.title }}**, {{ pub.venue_short }} {{ pub.year }}{% if pub.acceptance_rate != "" %} (Acceptance Rate: {{ pub.acceptance_rate }}){% endif %}{% if pub.note != "" %} ({{ pub.note }}){% endif %}
{% endunless %}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}

{% include visitor-map.html %}

## Collaboration
I welcome research collaborations in autonomous driving perception, trustworthy AI, and mobile/edge intelligence. If our interests overlap, please email me at [runw@clemson.edu](mailto:runw@clemson.edu).

</div>
