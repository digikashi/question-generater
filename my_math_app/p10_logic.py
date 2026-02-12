from p15_logic import is_p15_digit


def is_p10_digit(a, b):
    """
    1桁同士の計算がP10(基本の繰り上がり足し算)か判定する
    a: 現在の数 (被加数)
    b: 足す数 (加数)

    条件:
    1. 10への繰り上がりが発生する (a + b >= 10)
    2. P15(5玉分解)ではない
       -> 補数が5以上である OR
       -> 補数が5未満だが、1玉部分(a%5)だけで補数を引ける
    """
    # 繰り上がりがない場合は対象外
    if a + b < 10:
        return False

    # 補数 (足す数bに対する10の補数)
    complement = 10 - b

    # P15
    is_p15 = is_p15_digit(a, b)
    #is_p15 = (complement < 5) and ((a % 5) < complement)

    # P10は「繰り上がりがあるが、P15ではないもの」
    return not is_p15


def count_p10_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるP10の総数をカウントする
    terms: 計算する数値のリスト
    num_digits: 対象の桁数
    """
    sim = SorobanSimulator()

    # termsリストからシミュレーターに順次入力
    for val in terms:
        if val >= 0:
            sim.add(val)
        else:
            sim.subtract(abs(val))

    return sim.p10_count

    p10_count = 0
    current_sum = 0

    for val in terms[0:]:
        # 足し算の場合のみP10判定を行う
        if val > 0:
            # --- 一の位の判定 ---
            curr_ones = current_sum % 10
            val_ones = val % 10
            if is_p10_digit(curr_ones, val_ones):
                p10_count += 1

            # --- 十の位の判定 ---
            if num_digits >= 2:
                curr_tens = (current_sum // 10) % 10
                val_tens = (val // 10) % 10
                if is_p10_digit(curr_tens, val_tens):
                    p10_count += 1

            # --- 百の位の判定 ---
            if num_digits >= 3:
                curr_hundreds = (current_sum // 100) % 10
                val_hundreds = (val // 100) % 10
                if is_p10_digit(curr_hundreds, val_hundreds):
                    p10_count += 1

        # 計算を進める
        current_sum += val

    return p10_count


class SorobanSimulator:
    def __init__(self):
        # [一の位, 十の位, 百の位, 千の位...]
        self.digits = [0] * 10
        self.p10_count = 0
        self.history = []

    def get_value(self):
        val = 0
        for i, d in enumerate(self.digits):
            val += d * (10 ** i)
        return val

    def add(self, value):
        """数値を足し、P10をカウントする"""
        str_val = str(value)
        # 位ごとに処理するために逆順にする
        val_digits = [int(c) for c in str(str_val)[::-1]]

        carry = 0

        # 桁ごとの計算 (最大桁まで+キャリー分)
        for i in range(len(self.digits)):
            if i >= len(val_digits) and carry == 0:
                break

            # この桁に足すべき数 (入力値 + 下の桁からの繰り上がり)
            input_digit = val_digits[i] if i < len(val_digits) else 0

            # ステップ1: 入力値を足す
            current_digit = self.digits[i]
            if input_digit > 0:
                if is_p10_digit(current_digit, input_digit):
                    self.p10_count += 1
                    self.history.append(f"P10発生: {current_digit}+{input_digit} (桁:{10 ** i})")

                sum_val = current_digit + input_digit
                self.digits[i] = sum_val % 10
                step1_carry = sum_val // 10
            else:
                step1_carry = 0

            # ステップ2: 下の桁からの繰り上がり(carry)を足す
            # ※繰り上がりは常に「+1」の処理
            step2_carry = 0
            if carry > 0:
                current_digit_after_step1 = self.digits[i]
                # 9+1などの場合もP10判定を行う
                if is_p10_digit(current_digit_after_step1, carry):
                    self.p10_count += 1
                    self.history.append(f"P10発生(繰上): {current_digit_after_step1}+{carry} (桁:{10 ** i})")

                sum_val_2 = current_digit_after_step1 + carry
                self.digits[i] = sum_val_2 % 10
                step2_carry = sum_val_2 // 10

            # 次の桁への繰り上がりをセット
            carry = step1_carry + step2_carry

    def subtract(self, value):
        """数値を引く (P10カウントはしないが盤面を更新する)"""
        # 単純化のため、現在の総量から引いて、digitsを再構成する手法をとる
        # (厳密なM10/M5判定が必要ない場合はこれが確実)
        current_val = self.get_value()
        new_val = current_val - value

        if new_val < 0:
            raise ValueError("マイナス計算は未対応です")

        # digitsを更新
        s_val = str(new_val)[::-1]
        for i in range(len(self.digits)):
            if i < len(s_val):
                self.digits[i] = int(s_val[i])
            else:
                self.digits[i] = 0

    def process_expression(self, expression):
        # "30+56+..." のような文字列を解析
        import re
        tokens = re.findall(r'[+-]?\d+', expression)

        print(f"計算式: {expression}")
        print("-" * 20)

        for token in tokens:
            val = int(token)
            if val >= 0:
                # 足し算
                prev_val = self.get_value()
                self.add(val)
                print(f"ADD {val}: {prev_val} -> {self.get_value()} | P10累積: {self.p10_count}")
            else:
                # 引き算
                prev_val = self.get_value()
                self.subtract(abs(val))
                print(f"SUB {abs(val)}: {prev_val} -> {self.get_value()}")

        return self.p10_count
