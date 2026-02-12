def is_p5_digit(a, b):
    """
    1桁同士の計算がP5(5の合成)か判定する
    
    ユーザー定義のP5条件:
    1. 左辺(a)と右辺(b)が共に1以上4以下である
    2. a + b が5以上である
    
    例: (1,4), (2,3), (3,3), (4,4) など
    """
    # 範囲のチェック (1 <= x <= 4)
    is_in_range = (1 <= a <= 4) and (1 <= b <= 4)

    # 和のチェック (sum >= 5)
    is_sum_ge_5 = (a + b >= 5)

    return is_in_range and is_sum_ge_5

def count_p5_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるP5の総数をカウントする
    terms: 計算する数値のリスト (例: [12, 34, -5])
    num_digits: 対象の桁数（デフォルト2）
    """
    p5_count = 0
    current_sum = 0

    for val in terms[0:]:
        # 加算の場合のみP5判定を行う（そろばん等のロジックにおいて、P5は通常加算時の動作を指すため）
        if val > 0:
            # --- 一の位の判定 ---
            curr_ones = current_sum % 10
            val_ones = val % 10
            if is_p5_digit(curr_ones, val_ones):
                p5_count += 1

            # --- 十の位の判定 ---
            if num_digits >= 2:
                curr_tens = (current_sum // 10) % 10
                val_tens = (val // 10) % 10
                if is_p5_digit(curr_tens, val_tens):
                    p5_count += 1

            # --- 百の位の判定 ---
            if num_digits >= 3:
                curr_hundreds = (current_sum // 100) % 10
                val_hundreds = (val // 100) % 10
                if is_p5_digit(curr_hundreds, val_hundreds):
                    p5_count += 1

        # 計算を進める
        current_sum += val

    return p5_count