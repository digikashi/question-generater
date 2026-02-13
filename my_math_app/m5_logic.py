def is_m5_digit(a, b):
    """
    1桁同士の引き算がM5(Minus 5 / 5の分解)か判定する
    a: 引かれる数 (被減数)
    b: 引く数 (減数)
    
    条件:
    1. 引かれる数(a)が5以上である
    2. aの5余り(a-5)だけではbを引けない (b > a-5)
       -> つまり、5玉を使う必要がある
    3. 引き算として成立する (a >= b) ※マイナスにならない
    """
    # 5玉を持っているか
    has_five = (a >= 5)

    # 1玉部分だけで引けるか (引けないならM5)
    # 例: 6(5+1) - 2 -> 1 < 2 なのでTrue (5を使う)
    # 例: 6(5+1) - 1 -> 1 >= 1 なのでFalse (1玉で足りる)
    needs_five_decomposition = ((a - 5) < b)

    # 基本的な引き算の成立条件
    is_valid_sub = (a >= b)

    # bの範囲
    is_b_under_five = (1 <= b <= 4)

    return has_five and needs_five_decomposition and is_valid_sub and is_b_under_five

def count_m5_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるM5の総数をカウントする
    terms: 計算する数値のリスト (例: [5, -1, -2])
    num_digits: 対象の桁数（デフォルト2）
    """
    m5_count = 0
    current_sum = 0

    for val in terms[0:]:
        # 引き算（負の数）の場合のみM5判定を行う
        if val < 0:
            abs_val = abs(val)

            # --- 百の位の判定 ---
            if num_digits >= 3:
                curr_hundreds = (current_sum // 100) % 10
                val_hundreds = (abs_val // 100) % 10
                if val_hundreds > 0 and is_m5_digit(curr_hundreds, val_hundreds):
                    m5_count += 1

            # --- 十の位の判定 ---
            if num_digits >= 2:
                curr_tens = (current_sum // 10) % 10
                val_tens = (abs_val // 10) % 10
                if val_tens > 0 and is_m5_digit(curr_tens, val_tens):
                    m5_count += 1

            # --- 一の位の判定 ---
            curr_ones = current_sum % 10
            val_ones = abs_val % 10
            # 0を引く場合はカウントしない
            if val_ones > 0 and is_m5_digit(curr_ones, val_ones):
                m5_count += 1

        # 計算を進める
        current_sum += val

    return m5_count