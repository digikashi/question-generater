from m15_logic import is_m15_digit
# ※もしm15_logicがない場合は、このファイル内で同等の関数を定義しても動作します

def is_m10_digit(a, b):
    """
    1桁同士の計算がM10(基本の繰り下がり引き算)か判定する
    a: 引かれる数 (被減数)
    b: 引く数 (減数)
    
    条件:
    1. 繰り下がりが発生する (a < b)
    2. M15(補数加算時のP5)ではない
    """
    # 1. 繰り下がりチェック
    if a >= b:
        return False

    # 2. M15かどうかチェック
    # M15の条件: 
    #   補数(c=10-b)を足すときにP5が発生するか
    #   (a, cが共に1~4 かつ a+c>=5)
    
    return not is_m15_digit(a, b)

    complement = 10 - b

    # M15判定ロジックの再掲 (依存関係をなくすためここに記述)
    is_m15 = False
    if (1 <= a <= 4) and (1 <= complement <= 4):
        if a + complement >= 5:
            is_m15 = True

    # M15でなければM10
    return not is_m15

class SorobanSimulatorM10:
    def __init__(self):
        self.digits = [0] * 10
        self.m10_count = 0

    def add(self, value):
        """足し算 (盤面更新のみ)"""
        val_str = str(value)[::-1]
        carry = 0
        for i in range(len(self.digits)):
            val_digit = int(val_str[i]) if i < len(val_str) else 0
            sum_val = self.digits[i] + val_digit + carry
            self.digits[i] = sum_val % 10
            carry = sum_val // 10

    def subtract(self, value):
        """引き算 (M10カウントと盤面更新)"""
        val_str = str(value)[::-1]
        borrow = 0

        for i in range(len(self.digits)):
            # 処理不要なら終了
            if i >= len(val_str) and borrow == 0:
                break

            sub_digit = int(val_str[i]) if i < len(val_str) else 0

            # 現在の桁の値
            current_digit = self.digits[i]

            # 実際に引く値 (入力値 + 下の桁からの借り)
            # ※M10判定は「その桁での操作」を見るため、borrow込みの値で判定するか、
            #   純粋な入力値で判定するかは定義次第ですが、
            #   通常は「操作しようとした瞬間」の判定を行うため、
            #   ここでは厳密にシミュレートします。

            # 下の桁からのborrowがある場合、この桁から1引く操作が入る
            # その「1引く操作」自体がM10/M5/Sの対象になるが、
            # ここでは「入力値の引き算」におけるM10を主眼に置く。

            # シンプルな判定:
            # 「今ある値(current_digit)から、引くべき値(sub_digit)を引くときにM10になるか」
            # ※borrowの影響ですでに値が減っている場合は考慮済みとする

            # 引く操作がある場合のみ判定
            if sub_digit > 0:
                # すでに下の桁のborrow処理で値が変わっている可能性があるため
                # ここでは「borrow処理前の値」ではなく「現在の盤面値」で判定する
                if is_m10_digit(current_digit, sub_digit):
                    self.m10_count += 1

            # 計算実行（次の桁へのborrow計算）
            total_sub = sub_digit + borrow
            res = current_digit - total_sub
            if res < 0:
                self.digits[i] = res + 10
                borrow = 1
            else:
                self.digits[i] = res
                borrow = 0

def count_m10_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるM10の総数をカウントする
    """
    sim = SorobanSimulatorM10()

    for val in terms:
        if val >= 0:
            sim.add(val)
        else:
            sim.subtract(abs(val))

    return sim.m10_count