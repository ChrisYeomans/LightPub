from bs4 import BeautifulSoup as BS
from ebooklib import epub
import requests

class NovelFullBook:
    entry = ""
    book = epub.EpubBook()
    chapters = []
    chapter_titles = {}

    def __init__(self, entry):
        self.entry = entry

    def set_metadata(self):
        p = requests.get(self.entry).text
        s = BS(p, 'html.parser')

        title = s.find("h3", { "class" : "title" }).text
        self.book.set_identifier(''.join([e for e in title if e != ' ']))
        self.book.set_title(title)
        self.book.set_language("en")

        author = s.find("div", { "class" : "info" }).find("a").text
        self.book.add_author(author)

    def gen_chapter(self, link):
        p = requests.get(link).text
        s = BS(p, 'html.parser')
        a = s.find("div", { "id" : "chapter-content" })

        chap_title = [e for e in s.find("div", { "id" : "chapter-content" }).findAll("p") if e.text][0].text.strip()
        if chap_title in self.chapter_titles:
            self.chapter_titles[chap_title] += 1
            chap_title = chap_title+'('+str(self.chapter_titles[chap_title])+')'
        else:
            self.chapter_titles[chap_title] = 0
        stripped_chap_title = ''.join(chap_title.split())
        c = epub.EpubHtml(title=chap_title, file_name=stripped_chap_title+".xhtml")
        c.content = (str(a).encode('utf-8'))
        self.book.add_item(c)

        self.book.toc.append(
            epub.Link(stripped_chap_title+".xhtml", chap_title, chap_title),
        )
        self.chapters.append(c)

        next_chap_link = s.find("a", { "id" : "next_chap" }).get('href')
        return "https://novelfull.net" + next_chap_link if next_chap_link else ""
        
    def write_book(self):
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        self.book.spine = ["nav"] + self.chapters
        epub.write_epub(self.book.title + ".epub", self.book, {})


PAGE = "https://novelfull.net/invincible-divine-dragons-cultivation-system.html"
c1 = "https://novelfull.net/invincible-divine-dragons-cultivation-system/chapter-1-start-the-round-as-a-dragon.html"

a = NovelFullBook(PAGE)
a.set_metadata()
l = a.gen_chapter(c1)
while 1:
    if l:
        l = a.gen_chapter(l)
        print(l)
    else:
        break
a.write_book()
