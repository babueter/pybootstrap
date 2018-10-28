#!/usr/bin/python3
#
# Bootstrap Resume builder
#
# Configured via resume.conf

import sys
sys.path.append("bootstrap")

import argparse
import configparser
from pybootstrap.core import Component, Container, Attribute
from pybootstrap.collections import ProgressBar, Carousel, Table
from pybootstrap import utils


# You probably want FontAwesome-Pro...
script_fontawesome = Component(
    "link",
    inline=True,
    rel="stylesheet",
    src="https://use.fontawesome.com/releases/v5.4.1/css/all.css",
    integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz",
    crossorigin="anonymous",
)

script_bootstrap_min = Component(
    "script",
    inline=True,
    src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js",
    integrety="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy",
    crossorigin="anonymous",
)


script_jquery = Component(
    "script",
    inline=True,
    src="https://code.jquery.com/jquery-3.2.1.slim.min.js",
    integrety="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN",
    crossorigin="anonymous",
)

font_awesome_classes = {
    "Email": "fa fa-envelope",
    "LinkedIn": "fa fa-linkedin-square",
    "GitHub": "fa fa-github-square",
    "Stack-Overflow": "fa fa-stack-overflow",
    "Facebook": "fa fa-facebook-square",
    "Twitter": "fa fa-twitter-square",
    "Twitch": "fa fa-twitch",
    "Tumblr": "fa fa-tumblr",
    "Instagram": "fa fa-instagram",
}


def config_list(config, name, reverse=False):
    return sorted([
            x for x in config.keys()
            if x.startswith("{}-".format(name))
        ], key=lambda x: int(x.split('-')[1]), reverse=reverse
    )


class TitleBar(Container):
    def __init__(self, name, title, profile_pic=None):
        super().__init__(id="cv_titlebar")
        utils.add_class_attributes(self, "row", "p-3", "mb-2", "bg-primary", "text-white")

        self.body = Container(id="title_body")
        self.links = Table(id="title_links", rows=1, cols=2, border="0")

        if profile_pic:
            pic_col = Container(**{"class": "col-sm-2 align-self-center"})
            pic_col.add_component(Component("img", src=profile_pic, **{"class": "rounded-circle img-thumbnail"}))
            self.add_component(pic_col)
            utils.add_class_attributes(self.body, "col-sm-7")

        else:
            utils.add_class_attributes(self.body, "col-sm-9")

        self.links_container = Container(title="title_links_container")
        self.links_container.add_component(self.links)
        utils.add_class_attributes(self.links_container, "col-sm-3")

        self.body.add_component(Component("h3", id="title_body_name", text=name, inline=True))
        self.body.add_component(Component("h4", id="title_body_title", text=title, inline=True))
        self.body.add_component(Component("br"))
        self.add_component(self.body)
        self.add_component(self.links_container)

    def add_social_media(self, media, href):
        self.links.add_rows(1)
        row = self.links.rows()

        self.links.get_col(row, 1).add_component(Component("a", inline=True, text=media, style="color:white", href=href))
        utils.add_class_attributes(self.links.get_col(row, 1), "text-right")

        span = Container("span", title=media)
        if media in font_awesome_classes:
            font_awesome = Component("i", inline=True, style="color:white", **{"aria-hidden": "true"})
            utils.add_class_attributes(font_awesome, font_awesome_classes[media])
            href = Container("a", href=href)
            href.add_component(font_awesome)

        span.add_component(href)
        self.links.get_col(row, 2).add_component(span)


class SideBar(Container):
    INTERVAL=7

    def __init__(self):
        super().__init__(id="cv_sidebar")
        utils.add_class_attributes(self, "col-3", "p-3", "mb-2", "bg-secondary", "text-white")

        self.competencies = Carousel(pause_on_hover=True, controls=True, interval=int(self.INTERVAL*1000), ride="carousel")
        self.competencies.add_attribute(Attribute("style", "height: 200px;"))
        self.competencies.del_component(self.competencies.id + '-prev')
        self.competencies.get_component(self.competencies.id + '-next').add_attribute(Attribute("style", "height: 25%;"))
        utils.add_class_attributes(self.competencies.get_component(self.competencies.id + '-next'), "self-align-top")
        self.add_component(self.competencies)

        self.add_component(Component("br"))
        self.add_component(Component("h3", text="Personal Projects"))
        self.projects = Container("ul")
        self.add_component(self.projects)

    def add_competency(self, competency, skill, confidence):
        competency_section = self.get_component("competency-"+competency)
        if competency_section is None:
            competency_section = Container(id="competency-"+competency)
            competency_section.add_component(Component("h3", inline=True, text=competency))
            self.competencies.add_item(competency_section)

        skill_text = Component("small", text=skill, style="margin-left: 5px")
        utils.add_class_attributes(skill_text, "justify-content-left", "d-flex", "position-absolute", "w-100")

        skill_bar = ProgressBar(valuenow=confidence)
        utils.add_class_attributes(skill_bar, "m-1")
        skill_bar.get_component(skill_bar.id + '-progressbar').add_component(skill_text)
        competency_section.add_component(skill_bar)

    def add_project(self, text, href):
        list_item = Container("li")
        list_item.add_component(Component("a", href=href, text=text, **{"class": "text-white"}))
        self.projects.add_component(list_item)


class Job(Container):
    TECHNOLOGY_COLUMNS=3

    def __init__(self, config_section=None):
        id=None
        if config_section:
            id=config_section.name

        super().__init__(id=id)

        self._company = Component('h4')
        self._title = Component('h5')
        self._date = Component('u')

        self._technologies = Table(rows=1, cols=self.TECHNOLOGY_COLUMNS, id=self.id + '-technologies', border="0", cellpadding="5")
        self._bullets = Container("ul", id=self.id + '-bullets')
        self._accomplishments = Container(id=self.id + '-accomplishments')

        self.add_component(self._company)
        self.add_component(self._title)
        self.add_component(self._date)
        self.add_component(Component("br"))
        self.add_component(Component("b", inline=True, text="Technologies"))
        self.add_component(self._technologies)
        self.add_component(Component("br"))
        self.add_component(Component("b", inline=True, text="Responsibilities"))
        self.add_component(self._bullets)
        self.add_component(self._accomplishments)

        if config_section:
            self.update_components(config_section)

    def update_components(self, config_section):
        self._title.text = config_section['title']
        self._company.text = config_section['company']

        if config_section['to date']:
            self._date.text = config_section['from date'] + ' - ' + config_section['to date']
        else:
            self._date.text = config_section['from date']

        col=1
        row=1
        for technology in config_list(config_section, 'technology'):
            self._technologies.get_col(row, col).add_component(Component("div", inline=True, text=config_section[technology]))
            col+=1
            if col > self.TECHNOLOGY_COLUMNS:
                col=1
                row+=1
                self._technologies.add_rows(1)

        for bullet in config_list(config_section, 'bullet'):
            self._bullets.add_component(Component("li", text=config_section[bullet]))

        accomplishment_text = Component("b", text="accomplishment: ")
        for accomplishment in config_list(config_section, 'accomplishment'):
            accomplishment_html = Container()
            accomplishment_html.add_component(accomplishment_text)
            accomplishment_html.add_component(Component("i", text=config_section[accomplishment]))
            self._accomplishments.add_component(accomplishment_html)


class MainBody(Container):
    def __init__(self):
        super().__init__(id="cv_main_body")
        utils.add_class_attributes(self, "col-9", "p-3", "mb-2", "bg-light", "text-dark")
        self.add_component(Component("h3", inline=True, text="Work History"))


class CV(Container):
    def __init__(self, configfile):
        super().__init__(id="cv")
        utils.add_class_attributes(self, "container")

        self.process_config(configfile)
        self.update_components()

    def process_config(self, configfile):
        self.config = configparser.ConfigParser()
        self.config.optionxform=str
        self.config.read(configfile)

        for key in self.config['personal'].keys():
            setattr(self, key, self.config['personal'][key])

        self.title = "CV - " + self.name

    def update_components(self):
        self.clear_components()

        self._titlebar = TitleBar(self.name, self.job_title, self.image)
        self._sidebar = SideBar()
        self._mainbody = MainBody()

        self.add_component(self._titlebar)

        row = Container(**{"class": "row"})
        row.add_component(self._sidebar)
        row.add_component(self._mainbody)
        self.add_component(row)

        for key in self.config['social-media'].keys():
            self._titlebar.add_social_media(key, self.config['social-media'][key])

        for competency in [c for c in self.config.keys() if c.startswith('competency-')]:
            competency_name = competency.split('-')[1]
            for skill in self.config[competency].keys():
                self._sidebar.add_competency(competency_name, skill, int(self.config[competency][skill]))

        for project in [p for p in self.config.keys() if p.startswith('project-')]:
            self._sidebar.add_project(self.config[project]["text"], self.config[project]["link"])

        for job in config_list(self.config, "job", reverse=True):
            self._mainbody.add_component(Component("hr"))
            self._mainbody.add_component(Job(self.config[job]))


# Main Program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="file", default="resume.conf", nargs="?", help="Name of the config file to use")
    args = parser.parse_args()
    cv = CV(args.file)

    print(utils.Header(cv.title, script_jquery, script_bootstrap_min, script_fontawesome))
    print(cv)
    print(utils.Footer())
