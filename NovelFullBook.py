from bs4 import BeautifulSoup as BS
from os.path import basename
import pypub
import os
import requests

class NovelFullBook:
    entry: str = ""
    book: pypub.Epub = pypub.Epub("")
    chapters: list[any] = []
    chapter_titles: dict[str, int] = {}
    num_chapters: int = 0

    def __init__(self, entry: str):
        self.entry = entry
        self.chapters = []
        self.chapter_titles = {}
        self.num_chapters = 0
        self.book = pypub.Epub("")

    def set_metadata(self):
        p: str = requests.get(self.entry).text
        s: BS = BS(p, 'lxml')

        total_chapters_a = s.find("ul", { "class" : "pagination" }).find_all("li")[-1].find("a")
        total_chapters_num = int(total_chapters_a['href'].split("=")[-1])*50 - 25
        self.num_chapters = total_chapters_num
        title: str = s.find("h3", { "class" : "title" }).text
        author: str = s.find("div", { "class" : "info" }).find("a").text
        img_lnk: str = "https://novelfull.net" + s.find_all("img")[-1]['src']
        with open(basename("cover.png"), "wb") as f:
            f.write(requests.get(img_lnk).content)
        self.book = pypub.Epub(title, creator=author)
        self.book.builder.cover = basename("cover.png")
        self.book.builder.epub.cover = basename("cover.png")


    def gen_chapter(self, link: str) -> str:
        if not link:
            return ""
        p: str = requests.get(link).text
        s: BS = BS(p, 'lxml')
        a: BS = s.find("div", { "id" : "chapter-content" })

        chap_title_a: BS = s.find("a", { "class" : "chapter-title" })
        
        chap_title: str = bytes(chap_title_a['title'], 'utf-8').decode('utf-8', 'ignore')
        if chap_title in self.chapter_titles:
            self.chapter_titles[chap_title] += 1
            chap_title: str = chap_title+'('+str(self.chapter_titles[chap_title])+')'
        else:
            self.chapter_titles[chap_title] = 0
        c: pypub.Chapter = pypub.create_chapter_from_text(bytes(a.text, 'utf-8').decode('utf-8', 'ignore'), title=chap_title)
        ass: pypub.Assignment = self.book.assign_chapter()
        self.book.builder.render_chapter(ass, c)
        self.chapters.append(c)

        next_chap_link: str = s.find("a", { "id" : "next_chap" }).get('href')
        return "https://novelfull.net" + next_chap_link if next_chap_link else ""
        
    def write_book(self):
        self.set_metadata()
        p: str = requests.get(self.entry).text
        s: BS = BS(p, 'lxml')
        chap_1_a = s.find("ul", { "class" : "list-chapter" }).find("a")
        chap_1 = "https://novelfull.net" + chap_1_a['href']
        cntr = 1
        with self.book.builder as builder:
            dirs = builder.begin()
            l: str = self.gen_chapter(chap_1)
            while 1:
                if l:
                    yield cntr
                    cntr += 1
                    l = self.gen_chapter(l)
                else:
                    break
            self.book.builder.index()
            self.book.builder.finalize(self.book.title + ".epub")
        os.remove("cover.png")

if __name__ == "__main__":
    PAGE: str = "https://novelfull.net/journey-to-become-a-true-god.html"

    a: NovelFullBook = NovelFullBook(PAGE)
    a.write_book()