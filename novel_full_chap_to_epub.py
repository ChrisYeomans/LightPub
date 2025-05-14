from bs4 import BeautifulSoup as BS
import pypub
import requests

from typing import List

class NovelFullBook:
    entry: str = ""
    book: pypub.Epub = pypub.Epub("")
    chapters: list[any] = []
    chapter_titles: dict[str, int] = {}

    def __init__(self, entry: str):
        self.entry = entry

    def set_metadata(self):
        p: str = requests.get(self.entry).text
        s: BS = BS(p, 'html.parser')

        title: str = s.find("h3", { "class" : "title" }).text
        author: str = s.find("div", { "class" : "info" }).find("a").text
        self.book = pypub.Epub(title, creator=author)

    def gen_chapter(self, link: str) -> str:
        if not link:
            return ""
        p: str = requests.get(link).text
        s: BS = BS(p, 'html.parser')
        a: BS = s.find("div", { "id" : "chapter-content" })

        chap_title: List[str] = [e for e in s.find("div", { "id" : "chapter-content" }).findAll("p") if e.text][0].text.strip()
        if chap_title in self.chapter_titles:
            self.chapter_titles[chap_title] += 1
            chap_title: str = chap_title+'('+str(self.chapter_titles[chap_title])+')'
        else:
            self.chapter_titles[chap_title] = 0
        c: pypub.Chapter = pypub.create_chapter_from_text(a.text, title=chap_title)
        ass: pypub.Assignment = self.book.assign_chapter()
        self.book.builder.render_chapter(ass, c)
        # self.book.add_chapter(c)
        self.chapters.append(c)

        next_chap_link: str = s.find("a", { "id" : "next_chap" }).get('href')
        return "https://novelfull.net" + next_chap_link if next_chap_link else ""
        
    def write_book(self):
        self.book.builder.finalize(self.book.title + ".epub")


PAGE: str = "https://novelfull.net/a-villains-will-to-survive.html"
c1: str = "https://novelfull.net/a-villains-will-to-survive/chapter-1-prologue.html"

a: NovelFullBook = NovelFullBook(PAGE)
a.set_metadata()

with a.book.builder as builder:
    dirs = builder.begin()
    l: str = a.gen_chapter(c1)
    while 1:
        if l:
            l = a.gen_chapter(l)
            print(l)
        else:
            break
    a.write_book()
