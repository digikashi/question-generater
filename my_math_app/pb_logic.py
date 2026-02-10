def is_plus_basic_digit(a, b):
    """
    1桁同士の計算がPB(Plus Basic)か判定する
    条件1: a + b < 10 (10への繰り上がりなし)
    条件2: (a % 5) + (b % 5) < 5 (5への繰り上がりなし)
    """
    return (a + b < 10) and ((a % 5) + (b % 5) < 5)

def count_pb_in_sequence(terms):
    """
    計算過程に含まれるPBの総数をカウントする
    """
    pb_count = 0
    current_sum = 0

    for val in terms[0:]:
        # 加算の場合のみPB判定を行う
        if val > 0:
            # --- 一の位の判定 ---
            curr_ones = current_sum % 10
            val_ones = val % 10
            if is_plus_basic_digit(curr_ones, val_ones):
                pb_count += 1

            # --- 十の位の判定 ---
            # 現在の合計値の十の位（100以上になっても、計算に関与するのは十の位）
            curr_tens = (current_sum // 10) % 10
            val_tens = (val // 10) % 10
            if is_plus_basic_digit(curr_tens, val_tens):
                pb_count += 1

        # 計算を進める（引き算の場合も合計値は更新が必要）
        current_sum += val

    return pb_count
