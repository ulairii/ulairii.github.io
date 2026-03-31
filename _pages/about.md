---
permalink: /
title: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<div class="academic-home" markdown="1">

## Education Experience

<div class="academic-edu">
  <div class="academic-edu__item">
    <div class="academic-edu__head">
      <span class="academic-edu__school">Clemson University</span>
      <span class="academic-edu__place">Clemson, SC</span>
    </div>
    <div class="academic-edu__degree">Ph.D. Student in Computer Science</div>
    <div class="academic-edu__date">Aug. 2025 - Present</div>
    <div class="academic-edu__detail">Concentration: 3D Computer Vision, AI Security and Mobile Computing</div>
  </div>

  <div class="academic-edu__item">
    <div class="academic-edu__head">
      <span class="academic-edu__school">Carnegie Mellon University</span>
      <span class="academic-edu__place">Pittsburgh, PA</span>
    </div>
    <div class="academic-edu__degree">M.S. in Electrical and Computer Engineering (Applied Advanced Program)</div>
    <div class="academic-edu__date">Sep. 2021 - May 2023</div>
  </div>

  <div class="academic-edu__item">
    <div class="academic-edu__head">
      <span class="academic-edu__school">Rensselaer Polytechnic Institute</span>
      <span class="academic-edu__place">Troy, NY</span>
    </div>
    <div class="academic-edu__degree">B.S. in Computer &amp; Systems Engineering</div>
    <div class="academic-edu__date">Sep. 2017 - May 2021</div>
  </div>
</div>

## Research Topics
* 3D Vision
* AI Security
* Mobile Computing

## Selected Publications
{% assign featured_pubs = site.data.publications.publications | where: "featured", true | sort: "date" | reverse %}
{% for pub in featured_pubs limit: 5 %}
{% assign styled_authors = pub.authors | replace: "Run Wang", "<span class='name-underline'>Run Wang</span>" %}
* **{{ pub.title }}**. {{ styled_authors }}. <span class="conference-highlight">{{ pub.venue_short | default: pub.venue }}</span>, {{ pub.year }}{% if pub.acceptance_rate and pub.acceptance_rate != "" %} (Acceptance Rate: {{ pub.acceptance_rate }}){% endif %}{% if pub.url and pub.url != "" %}. [Link]({{ pub.url }}){% endif %}
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
