class LexPositionService:

    MAX_CHAR = 0x10FFFF

    def mid_string(self, s1: str, s2: str) -> str:
        if not s1:
            s1 = ""
        if not s2:
            s2 = chr(self.MAX_CHAR)
        i = 0
        res = ""
        while True:
            c1 = ord(s1[i]) if i < len(s1) else 0
            c2 = ord(s2[i]) if i < len(s2) else self.MAX_CHAR
            mid = (c1 + c2) // 2
            res += chr(mid)
            if mid != c1:
                break
            i += 1
        return res

    def new_position_after(self, prev: str) -> str:
        return self.mid_string(prev, "")

    def new_position_before(self, next_: str) -> str:
        return self.mid_string("", next_)

    def new_position_between(self, prev: str, next_: str) -> str:
        return self.mid_string(prev, next_)
