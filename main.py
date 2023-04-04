from tkinter import Tk, Frame, BOTH, Label, LEFT, Entry, X, Button, RIGHT, Text, TOP, RAISED, StringVar, END
from tkinter.ttk import Notebook, Style, Progressbar
from src.aes_encrypt import AESCipher
from src.enhanced_algo import AudioSteganography


def main():
    root = Tk()
    app = FirstFrame(root)
    root.title("Audio Steganography")
    root.mainloop()


class FirstFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.window_()

    def initUI(self):
        self.parent.title("Audio Steganography")
        self.pack(fill=BOTH, expand=True)

        notebook = Notebook(self)
        # Tabs
        frame1 = Frame(width=800, height=600, relief=RAISED)
        frame2 = Frame(width=800, height=600)
        # frame3 = Frame(width=800, height=600)

        # variables
        self.audio_path = StringVar()
        self.newname = StringVar()
        self.audio_dec = StringVar()
        self.notice = StringVar()
        self.pwd = StringVar()
        self.showmsg = StringVar()
        self.dec_pass = StringVar()
        self.ori_audio = StringVar()
        self.enc_audio = StringVar()
        self.cal = StringVar()

        notebook.add(frame1, text="Encode")
        notebook.add(frame2, text="Decode")
        # notebook.add(frame3, text="Analysis")
        notebook.pack(pady=5)
        self.encode_screen(frame1)
        self.decode_screen(frame2)
        # self.analysis_screen(frame3)

    def decode_screen(self, parent):
        lbl = Label(parent, text="File Path:")
        lbl.grid(row=0, column=0)
        entry = Entry(parent, textvariable=self.audio_dec)
        entry.grid(row=0, column=2)

        lbl = Label(parent, text="Password :")
        lbl.grid(row=2, column=0)
        entry = Entry(parent, textvariable=self.dec_pass)
        entry.grid(row=2, column=2)
        encode = Button(parent, text="Decode", command=self.decode)
        encode.grid(row=3, column=1, padx=2)

        ss = Label(parent, textvariable=self.showmsg)
        ss.grid(row=5, column=3)

    def encode_screen(self, parent):
        self.pb = Progressbar(
            parent,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        Label(parent, textvariable=self.notice).grid(row=10, column=6)
        lbl = Label(parent, text="File Path:")
        lbl.grid(row=1, column=0)
        entry = Entry(parent, textvariable=self.audio_path)
        entry.grid(row=1, column=2)

        lb0 = Label(parent, text="key file name:")
        lb0.grid(row=1, column=4)
        entry0 = Entry(parent, textvariable=self.newname)
        entry0.grid(row=1, column=6)

        lb0 = Label(parent, text="password:")
        lb0.grid(row=2, column=4)
        entry0 = Entry(parent, textvariable=self.pwd)
        entry0.grid(row=2, column=6)

        lb2 = Label(parent, text="Message:")
        lb2.grid(row=3, column=0, padx=5)
        self.mess = Text(parent, width=50, height=15)
        self.mess.grid(row=3, column=1, rowspan=4, columnspan=4)

        # Encode button

        encode = Button(parent, text="Encode", command=self.encode)
        encode.grid(row=8, column=2, padx=2)

    def decode(self):
        s = self.audio_dec.get()
        p = self.dec_pass.get()

        if s == "" or p == "":
            return 0

        decrypt = AudioSteganography()
        retrived = decrypt.extract(s)
        key = retrived.split("*")[0]

        msg = f"Message encrypted in the Image is: \n {retrived.split('*')[0]}"
        key_byte = bytes(key.encode("ascii"))
        print(key_byte)
        data = AESCipher(p).decrypt(key_byte)
        self.audio_dec.set("")
        self.dec_pass.set("")

        self.showmsg.set(data)


    def encode(self):


        audio_path = self.audio_path.get()
        message = self.mess.get("1.0", "end-1c")
        newfile = self.newname.get()
        pwd = self.pwd.get()


        if audio_path == "" or message == "" or newfile == "" or pwd == "":
            return 0

        self.pb.grid(row=10, column=2)
        self.notice.set("Encoding...")
        self.pb.start(5)
        aes = AESCipher(pwd).encrypt(message)
        encrypt = AudioSteganography()
        encrypt.embed(audio_path, aes.decode("ascii"), newfile)

        # cipher_text = Cipher(message)
        # ctect = cipher_text.getKey()
        # enc = Steg()

        # db.save_key(ctect[0],ctect[1],ctect[2],ctect[3],pwd)

        # enc.msg_Embed(audio_path, str(ctect[0]), newfile)
        self.pb.stop()
        self.notice.set("sucess")

    def window_(self):
        w = 800
        h = 600
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


if __name__ == '__main__':
    main()
