def is_minus_basic_digit(a, b):
    """
    1桁同士の引き算がMB(Minus Basic)か判定する
    a: 引かれる数 (current_sumの位)
    b: 引く数 (valの位)
    
    条件: (a // 5 >= b // 5) and (a % 5 >= b % 5)
    これは「5の分解」も「繰り下がり」も発生しない（そのまま引ける）条件です。
    """
    return (a // 5 >= b // 5) and (a % 5 >= b % 5)

def count_mb_in_sequence(terms, num_digits=2):
    """
    計算過程に含まれるMBの総数をカウントする（口単位）
    一の位がMBでなければ、その行はMBとしてカウントせず、十の位の判定もスキップする。
    """
    mb_count = 0
    current_sum = 0

    for val in terms[0:]:
        # 引き算(負の数)の場合のみMB判定を行う
        if val < 0:
            abs_val = abs(val)

            # --- 一の位の判定 ---
            curr_ones = current_sum % 10
            val_ones = abs_val % 10

            # 一の位がMB条件を満たさない場合
            if is_minus_basic_digit(curr_ones, val_ones):
                mb_count += 1

            # --- 十の位の判定 ---
            curr_tens = (current_sum // 10) % 10
            val_tens = (abs_val // 10) % 10

            # 一の位がOK、かつ十の位もOKならカウント
            if is_minus_basic_digit(curr_tens, val_tens):
                mb_count += 1

        # 計算を進める
        current_sum += val

    return mb_count