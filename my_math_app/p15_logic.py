def is_p15_digit(a, b):
    """
    1桁同士の計算がP15(複合足し算)か判定する
    a: 現在の数 (被加数)
    b: 足す数 (加数)

    条件:
    1. 10への繰り上がりが発生する (a + b >= 10)
    2. 補数(10-b)を引く際に、5玉の分解(M5のような動き)が発生する
       -> aが5以上である
       -> aの1玉部分(a-5)だけでは補数を引けない (a-5 < 補数)
       -> 補数が5ではない (補数が5の場合は単なる5払いになるためP15ではない)
    """
    # 繰り上がりがない場合は対象外
    if a + b < 10:
        return False

    # 補数 (足す数bに対する10の補数)
    complement = 10 - b
    if complement > 4:
        return False

    # 条件判定
    # 1. 5玉を持っている (a >= 5)
    # 2. 1玉だけでは補数を引けない (a - 5 < complement)
    # 3. 補数が5ではない (complement != 5) ※(5,5)などは除外
    has_five = (a >= 5)
    needs_split = (has_five and (a - 5) < complement)
    not_simple_five_sub = (complement != 5)

    return needs_split and not_simple_five_sub

def count_p15_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるP15の総数をカウントする
    terms: 計算する数値のリスト
    num_digits: 対象の桁数
    """
    p15_count = 0
    current_sum = 0

    for val in terms[0:]:
        # 足し算の場合のみP15判定を行う
        if val > 0:
            # --- 一の位の判定 ---
            curr_ones = current_sum % 10
            val_ones = val % 10
            if is_p15_digit(curr_ones, val_ones):
                p15_count += 1

            # --- 十の位の判定 ---
            if num_digits >= 2:
                curr_tens = (current_sum // 10) % 10
                val_tens = (val // 10) % 10
                if is_p15_digit(curr_tens, val_tens):
                    p15_count += 1

            # --- 百の位の判定 ---
            if num_digits >= 3:
                curr_hundreds = (current_sum // 100) % 10
                val_hundreds = (val // 100) % 10
                if is_p15_digit(curr_hundreds, val_hundreds):
                    p15_count += 1

        # 計算を進める
        current_sum += val

    return p15_count