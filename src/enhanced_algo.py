import wave

class AudioSteganography:
    max_bit = 4800

    def extract(self, audio_name):
        audio = wave.open(audio_name, mode='rb')
        audio_Frames_Bytes = bytearray(list(audio.readframes(audio.getnframes())))
        LF = int(len(audio_Frames_Bytes))
        position = self.select_embeded_position(self.max_bit,LF,self.midpoint_circle(2, 1, int(LF / 2)))
        extract = self.undo_lsb(audio_Frames_Bytes, position)
        str_extract = self.into_String(extract)

        return str_extract

    def embed(self, audio_name, text_msg, file):
        max_content = 600
        audio = wave.open(audio_name, mode='rb')
        audio_Frames_Bytes = bytearray(list(audio.readframes(audio.getnframes())))
        LF = int(len(audio_Frames_Bytes))

        text_msg = text_msg + (int(abs(len(text_msg) - max_content)) * "*")

        msg_bits_array = self.into_Bits_Array(text_msg)

        positions = self.select_embeded_position(self.max_bit, LF, self.midpoint_circle(2, 1, int(LF / 2)))

        # print(len(msg_bits_array))

        embed = self.do_lsb(msg_bits_array, audio_Frames_Bytes, positions)

        with wave.open("output/" + file, mode='wb') as sm:
            sm.setparams(audio.getparams())
            sm.writeframes(embed)
        audio.close()

    def into_Bits_Array(self, string):

        string_bits = ""
        for i in string:
            string_bits = string_bits + bin(ord(i)).lstrip('0b').rjust(8, "0")
        text_msg_bits_array = list(map(int, "".join(string_bits)))
        return (text_msg_bits_array)

    def is_int(self, num):
        '''
        :param num: Number
        :return: Bool
        '''
        try:
            int(num)
            return True
        except:
            return False

    def select_embeded_position(self, LT, LF, points):
        '''
        :param LT: length of Text
        :param LF: length of Audio-frames
        :param points: midpoint distance generated points
        :return: list
        '''

        data_locale = []

        for i in points:
            if abs(i[1]) not in data_locale and abs(i[1]) <= LF and self.is_int(abs(i[1])):
                data_locale.append(abs(i[1]))

            if LT == len(data_locale): break
        return data_locale

    def do_lsb(self, msg_bits, frame_bytes, positions):

        '''

        :param msg_bits: text in bit
        :param frame_bytes: audio frames in bytes
        :param positions: list of positions
        :return: frame bytes
        '''

        for i, bit in enumerate(msg_bits):
            frame_bytes[int(positions[i])] = (frame_bytes[int(positions[i])] & 254) | bit
        return (bytes(frame_bytes))

    def undo_lsb(self, frame_bytes, position):
        '''
        :param frame_bytes: audio frame bytes
        :param position: embeded position
        :return: Bool
        '''

        data = []
        for i in range(len(position)):
            data.append((frame_bytes[position[i]] & 1))
        return (data)

    def into_String(self, bytes):
        '''
        :param bytes: binary array
        :return: strings
        '''

        string_bits = ""
        for i in range(0, len(bytes), 8):
            string_bits = string_bits + chr(int("".join(map(str, bytes[i:i + 8])), 2))
        text_string_bits = "".join(string_bits)

        return (text_string_bits)

    def midpoint_circle(self, x_center, y_center, radius):
        '''
        :param x_center:
        :param y_center:
        :param radius:
        :return: points
        '''
        x = 0
        y = radius
        d = 1 - radius
        points = []
        while y >= x:
            points.append((x_center + x, y_center + y))
            points.append((x_center + y, y_center + x))
            points.append((x_center - x, y_center + y))

            points.append((x_center - y, y_center + x))

            points.append((x_center + x, y_center - y))

            points.append((x_center + y, y_center - x))

            points.append((x_center - x, y_center - y))

            points.append((x_center - y, y_center - x))
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
        return points
