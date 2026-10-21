# ANDROMEDA 7.0 · GALAXY — versión móvil inicial
# Interfaz Kivy. Datos guardados localmente en el almacenamiento privado de la app.
import json, os, threading, urllib.parse, urllib.request, urllib.error
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.utils import platform

BG = (0.025, 0.03, 0.045, 1)
PANEL = (0.055, 0.065, 0.09, 1)
BLUE = (0.16, 0.48, 1, 1)
WHITE = (0.94, 0.96, 1, 1)
MUTED = (0.58, 0.62, 0.70, 1)

def request_json(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent":"AndromedaGalaxy/7.0 (Android app)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

class AndromedaMobile(App):
    title = "ANDROMEDA"
    def build(self):
        Window.clearcolor = BG
        self.data_dir = self.user_data_dir
        self.chats_path = os.path.join(self.data_dir, "andromeda_chats.json")
        self.mem_path = os.path.join(self.data_dir, "andromeda_memoria.json")
        self.history_path = os.path.join(self.data_dir, "andromeda_historial.json")
        self.config_path = os.path.join(self.data_dir, "andromeda_config.json")
        self.chats = self._load(self.chats_path, [])
        self.memory = self._load(self.mem_path, {"hechos": [], "estadisticas":{"mensajes":0,"consultas_web":0}})
        self.history = self._load(self.history_path, [])
        self.config = self._load(self.config_path, {"idioma":"es","fuente_wikipedia":True,"fuente_duckduckgo":True,"fuente_wikidata":True,"fuente_openlibrary":True,"fuente_archive":True,"buscar_imagenes":True})
        self.busy = False
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        header = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        logo = Label(text="[b]ANDROMEDA[/b]", markup=True, font_size="22sp", color=WHITE, halign="left")
        logo.bind(size=lambda w,s: setattr(w,"text_size",s))
        version = Label(text="7.0 · GALAXY", font_size="11sp", color=BLUE, size_hint_x=None, width=dp(90))
        header.add_widget(logo); header.add_widget(version); root.add_widget(header)
        self.status = Label(text="Asistente personal · búsquedas abiertas · memoria local", color=MUTED, font_size="12sp", size_hint_y=None, height=dp(30), halign="left")
        self.status.bind(size=lambda w,s: setattr(w,"text_size",s))
        root.add_widget(self.status)
        tools = GridLayout(cols=3, size_hint_y=None, height=dp(42), spacing=dp(6))
        for txt, cb in [("Nuevo chat",self.new_chat),("Memoria",self.show_memory),("Acerca de",self.about)]:
            tools.add_widget(self.btn(txt,cb,small=True))
        root.add_widget(tools)
        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        self.messages = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=(0,dp(8)))
        self.messages.bind(minimum_height=self.messages.setter("height"))
        self.scroll.add_widget(self.messages); root.add_widget(self.scroll)
        compose = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(8))
        self.entry = TextInput(hint_text="Pregúntale algo a Andromeda…", multiline=False, background_color=PANEL, foreground_color=WHITE, hint_text_color=MUTED, cursor_color=BLUE, padding=(dp(12),dp(15)))
        self.entry.bind(on_text_validate=lambda *_: self.send())
        send = self.btn("Enviar", self.send)
        send.size_hint_x=None; send.width=dp(82)
        compose.add_widget(self.entry); compose.add_widget(send); root.add_widget(compose)
        if not self.chats:
            self.add_message("ANDROMEDA", "Hola. Soy ANDROMEDA 7.0 para Android. Puedo consultar fuentes abiertas, guardar tus chats y recordar datos que me indiques. Las funciones avanzadas de la versión de Windows se están adaptando.")
        else:
            for item in self.chats[-80:]:
                self.add_message(item.get("role","ANDROMEDA"), item.get("text",""), save=False)
        return root

    def btn(self, text, callback, small=False):
        b=Button(text=text, size_hint_y=None, height=dp(40 if small else 48), background_normal="", background_color=BLUE if not small else PANEL, color=WHITE, font_size="13sp")
        b.bind(on_release=lambda *_: callback())
        return b

    def add_message(self, role, text, save=True):
        color = BLUE if role in ("TÚ","USER") else WHITE
        lbl=Label(text=f"[b]{role}[/b]\n{text}", markup=True, color=color, font_size="14sp", size_hint_y=None, halign="left", valign="top", padding=(dp(12),dp(10)))
        lbl.bind(width=lambda w,v: setattr(w,"text_size",(v[0]-dp(24),None)))
        lbl.bind(texture_size=lambda w,v: setattr(w,"height",v[1]+dp(20)))
        from kivy.graphics import Color, RoundedRectangle
        with lbl.canvas.before:
            Color(*PANEL)
            lbl._bg=RoundedRectangle(pos=lbl.pos,size=lbl.size,radius=[dp(10)])
        lbl.bind(pos=lambda w,p:setattr(w._bg,"pos",p), size=lambda w,s:setattr(w._bg,"size",s))
        self.messages.add_widget(lbl)
        if save:
            self.chats.append({"role":role,"text":text,"time":datetime.now().isoformat(timespec="seconds")})
            self.chats=self.chats[-300:]
            self._save(self.chats_path,self.chats)
        Clock.schedule_once(lambda *_: setattr(self.scroll,"scroll_y",0),0.1)

    def send(self):
        text=self.entry.text.strip()
        if not text or self.busy: return
        self.entry.text=""; self.add_message("TÚ",text)
        self.busy=True; self.status.text="Buscando información…"
        threading.Thread(target=self.answer_worker,args=(text,),daemon=True).start()

    def answer_worker(self, query):
        try:
            answer, sources, image_url = self.answer_query(query)
            Clock.schedule_once(lambda dt:self.finish_answer(query,answer,sources,image_url),0)
        except Exception as e:
            detail = str(e)[:180]
            Clock.schedule_once(lambda dt, detail=detail:self.finish_answer(query,"No pude completar la búsqueda. Comprueba tu conexión a internet e inténtalo de nuevo.\nDetalle: "+detail,[],None),0)

    def answer_query(self, query):
        q=urllib.parse.quote(query)
        results=[]
        # Wikipedia search API
        if self.config.get("fuente_wikipedia",True):
            try:
                data=request_json("https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch="+q+"&format=json&utf8=1")
                for x in data.get("query",{}).get("search",[])[:3]:
                    results.append(("Wikipedia",x["title"],self.strip_html(x.get("snippet","")), "https://es.wikipedia.org/wiki/"+urllib.parse.quote(x["title"].replace(" ","_"))))
            except Exception: pass
        # DuckDuckGo Instant Answer (may return no results for many queries)
        if self.config.get("fuente_duckduckgo",True):
            try:
                d=request_json("https://api.duckduckgo.com/?q="+q+"&format=json&no_html=1&skip_disambig=1")
                if d.get("AbstractText"):
                    results.append(("DuckDuckGo",d.get("Heading") or query,d["AbstractText"],d.get("AbstractURL","https://duckduckgo.com/?q="+q)))
                for topic in d.get("RelatedTopics",[])[:3]:
                    if isinstance(topic,dict) and topic.get("Text"):
                        results.append(("DuckDuckGo",topic.get("FirstURL","Resultado"),topic["Text"],topic.get("FirstURL","")))
            except Exception: pass
        # Wikidata entity search
        if self.config.get("fuente_wikidata",True):
            try:
                d=request_json("https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+q+"&language=es&uselang=es&format=json")
                for x in d.get("search",[])[:2]:
                    desc=x.get("description","")
                    results.append(("Wikidata",x.get("label",query),desc,"https://www.wikidata.org/wiki/"+x.get("id","")))
            except Exception: pass
        # Open Library book search
        if self.config.get("fuente_openlibrary",True) and any(w in query.lower() for w in ["libro","libros","autor","novela","book"]):
            try:
                d=request_json("https://openlibrary.org/search.json?q="+q+"&limit=3")
                for x in d.get("docs",[])[:3]:
                    results.append(("Open Library",x.get("title","Libro"),", ".join(x.get("author_name",[])[:3]),"https://openlibrary.org"+x.get("key","")))
            except Exception: pass
        # Internet Archive search
        if self.config.get("fuente_archive",True) and any(w in query.lower() for w in ["archivo","documental","internet archive","libro antiguo"]):
            try:
                d=request_json("https://archive.org/advancedsearch.php?q="+q+"&fl[]=title&fl[]=identifier&rows=3&page=1&output=json")
                for x in d.get("response",{}).get("docs",[])[:3]:
                    results.append(("Internet Archive",x.get("title","Archivo"),"Recurso digital abierto","https://archive.org/details/"+x.get("identifier","")))
            except Exception: pass
        # Prefer useful result descriptions, remove duplicates
        unique=[]; seen=set()
        for r in results:
            key=(r[0],r[1])
            if key not in seen and (r[2] or r[3]): unique.append(r); seen.add(key)
        if unique:
            lines=[]
            for src,title,desc,url in unique[:6]:
                lines.append(f"• {title} — {desc[:500] if desc else 'Consulta la fuente para más información'}\n  Fuente: {src}"+(f"\n  {url}" if url else ""))
            answer="Encontré información en fuentes abiertas. Revisa las fuentes para verificar los datos:\n\n"+"\n\n".join(lines)
        else:
            answer="No encontré una respuesta fiable en las fuentes consultadas. Prueba reformulando la pregunta o con un tema más específico."
        # Wikimedia image search, best-effort
        image_url=None
        if self.config.get("buscar_imagenes",True):
            try:
                d=request_json("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch="+q+"&gsrnamespace=6&gsrlimit=1&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json")
                pages=d.get("query",{}).get("pages",{})
                for page in pages.values():
                    info=(page.get("imageinfo") or [{}])[0]
                    image_url=info.get("thumburl") or info.get("url")
                    if image_url: break
            except Exception: pass
        self.memory.setdefault("estadisticas",{}).setdefault("consultas_web",0)
        self.memory["estadisticas"]["consultas_web"]+=1
        return answer, unique[:6], image_url

    def finish_answer(self, query, answer, sources, image_url):
        self.busy=False; self.status.text="Listo · los chats y la memoria se guardan en este dispositivo"
        self.add_message("ANDROMEDA",answer)
        self.history.append({"pregunta":query,"respuesta":answer,"time":datetime.now().isoformat(timespec="seconds")})
        self.history=self.history[-300:]
        self.memory.setdefault("estadisticas",{}).setdefault("mensajes",0)
        self.memory["estadisticas"]["mensajes"]+=1
        self._save(self.history_path,self.history); self._save(self.mem_path,self.memory)
        if image_url:
            try:
                im=AsyncImage(source=image_url, size_hint_y=None, height=dp(220), allow_stretch=True)
                self.messages.add_widget(im)
                Clock.schedule_once(lambda *_: setattr(self.scroll,"scroll_y",0),0.1)
            except Exception: pass

    def new_chat(self):
        self.chats=[]
        self._save(self.chats_path,self.chats)
        self.messages.clear_widgets()
        self.add_message("ANDROMEDA","Nuevo chat. ¿Qué quieres investigar?")

    def show_memory(self):
        stats=self.memory.get("estadisticas",{})
        facts=self.memory.get("hechos",[])
        msg=f"Memoria local\n\nMensajes: {stats.get('mensajes',0)}\nConsultas web: {stats.get('consultas_web',0)}\nDatos guardados: {len(facts)}\n\nLos datos se guardan dentro del almacenamiento privado de esta app."
        Popup(title="Memoria de ANDROMEDA",content=Label(text=msg,color=WHITE),size_hint=(.88,.5),background_color=PANEL).open()

    def about(self):
        Popup(title="ANDROMEDA 7.0 · GALAXY",content=Label(text="Versión móvil inicial gratuita.\nBúsquedas: Wikipedia, DuckDuckGo, Wikidata,\nOpen Library, Internet Archive y Wikimedia Commons.\n\nNo utiliza una API de IA de pago.",color=WHITE),size_hint=(.88,.5),background_color=PANEL).open()

    @staticmethod
    def strip_html(s):
        import re, html
        return html.unescape(re.sub("<[^>]+>"," ",s)).replace("  "," ").strip()

    @staticmethod
    def _load(path, default):
        # Primero usa los datos privados actuales; en la primera ejecución puede importar
        # el JSON original que se empaquetó junto a main.py.
        for candidate in (path, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(path))):
            try:
                with open(candidate,"r",encoding="utf-8") as f: return json.load(f)
            except Exception: pass
        return default

    @staticmethod
    def _save(path, value):
        try:
            with open(path,"w",encoding="utf-8") as f: json.dump(value,f,ensure_ascii=False,indent=2)
        except Exception: pass

if __name__ == "__main__":
    AndromedaMobile().run()
