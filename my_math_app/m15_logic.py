def is_m15_digit(a, b):
    """
    1桁同士の引き算がM15(5玉合成を伴う繰り下がり)か判定する
    a: 引かれる数 (被減数)
    b: 引く数 (減数)
    
    条件:
    1. 引けない (a < b) -> 繰り下がり発生
    2. 補数加算時にP5(5の合成)が発生する
       -> 補数(10-b)が4以下である (つまり b >= 6)
       -> a が4以下である (5玉を使っていない)
       -> a + 補数 >= 5
    """
    # 引ける場合は対象外 (繰り下がりなし)
    if a >= b:
        return False

    complement = 10 - b

    # 条件判定
    # 1. 補数が4以下 (yが6以上でないと、補数が5以上になりP5条件を満たさない)
    if complement > 4:
        return False

    # 2. aが4以下 (元々5玉があったら、それは単なる加算になる)
    if not (1 <= a <= 4):
        return False

    # 3. 足して5以上 (P5発生)
    if a + complement < 5:
        return False

    return True


class SorobanSimulatorM15:
    def __init__(self):
        self.digits = [0] * 10
        self.m15_count = 0

    def add(self, value):
        """足し算 (M15カウントはしないが盤面更新)"""
        val_str = str(value)[::-1]
        carry = 0
        for i in range(len(self.digits)):
            val_digit = int(val_str[i]) if i < len(val_str) else 0

            # 単純な足し算シミュレーション
            sum_val = self.digits[i] + val_digit + carry
            self.digits[i] = sum_val % 10
            carry = sum_val // 10

    def subtract(self, value):
        """引き算 (M15をカウントして盤面更新)"""
        val_str = str(value)[::-1]
        borrow = 0

        for i in range(len(self.digits)):
            # 処理する桁が入力の範囲を超えて、かつBorrowもなければ終了
            if i >= len(val_str) and borrow == 0:
                break

            sub_digit = int(val_str[i]) if i < len(val_str) else 0

            # 現在の桁の値
            current_digit = self.digits[i]

            # 引く値 (入力値 + 下の桁からの借り)
            total_sub = sub_digit + borrow

            # ここで厳密な桁ごとのM15判定を行う
            # 注意: total_subが10を超えることは稀だが、borrowがあるため
            # 基本的には current_digit - total_sub を考える

            # ケース1: 入力値そのものの引き算によるM15
            # borrowの影響を含めるか議論があるが、そろばん操作としては
            # 「まず値を引く、足りなければ借りる」なので、
            # ここではシンプルに (current vs sub_digit) で判定する
            # ただし、すでに下の桁でborrowが発生している場合、
            # この桁は「1減っている」状態からスタートするのが厳密だが、
            # M15の定義は「その桁の操作」に焦点を当てる。

            # 簡易シミュレーションとして、「現在の見た目の数字」に対して引く
            if sub_digit > 0:
                # 下の桁からのborrow処理前の値で判定
                if is_m15_digit(current_digit, sub_digit):
                    self.m15_count += 1

            # 計算実行
            res = current_digit - total_sub
            if res < 0:
                self.digits[i] = res + 10
                borrow = 1
            else:
                self.digits[i] = res
                borrow = 0


def count_m15_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるM15の総数をカウントする
    """
    sim = SorobanSimulatorM15()

    for val in terms:
        if val >= 0:
            sim.add(val)
        else:
            sim.subtract(abs(val))

    return sim.m15_count
