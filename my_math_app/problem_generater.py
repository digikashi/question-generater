import random
from pb_logic import count_pb_in_sequence
from mb_logic import count_mb_in_sequence
from p5_logic import count_p5_in_sequence
from m5_logic import count_m5_in_sequence
from p10_logic import count_p10_in_sequence
from m10_logic import count_m10_in_sequence
from p15_logic import count_p15_in_sequence
from m15_logic import count_m15_in_sequence


def create_digits_pool(num_digits, num_lines, zero_count):
    # 1～9の数字をほぼ均等に配置した数字プールを生成
    normal_lines = num_lines - zero_count  # 通常の項の数 = 全口数 - 0の項の数

    # 必要な数字 = (通常の項 * 2個) + (0の項 * 1個)
    total_needed = (normal_lines * num_digits) + (zero_count * (num_digits - 1))

    # 1～9の数字をほぼ均等に配置
    base_count = total_needed // 9
    remainder = total_needed % 9

    digits_pool = []
    for i in range(1, 10):
        digits_pool.extend([i] * base_count)
    if remainder > 0:
        extra_candidates = random.choices(range(1, 10), k=remainder)  # 条件緩和のためにchoicesを使用
        digits_pool.extend(extra_candidates)

    return digits_pool


def create_zero_terms(current_pool, zero_count, num_digits):
    """
    プールから数字を取り出し、0を含む項を生成する
    2桁の場合: X0
    3桁の場合: XX0 または X0X (ランダム)
    """
    zero_terms = []
    for _ in range(zero_count):
        if num_digits == 2:
            val = current_pool.pop()
            term = val * 10 + 0

        elif num_digits == 3:
            h = current_pool.pop()
            other = current_pool.pop()
            pattern = random.choice(['XX0', 'X0X'])
            if pattern == 'XX0':
                term = h * 100 + other * 10 + 0
            else:
                term = h * 100 + 0 * 10 + other

        else:
            raise ValueError(f"create_zero_terms は現在 {num_digits} 桁に対応していません。")

        zero_terms.append(term)

    return zero_terms


def create_non_zero_terms(current_pool, num_digits):
    if len(current_pool) % num_digits != 0:
        raise ValueError(
            f"create_non_zero_terms エラー: プールの残り要素数({len(current_pool)}個)が桁数({num_digits})で割り切れません。組み合わせを作成できません。")

    # 指定桁数の数字セットを生成（最大50回試行）
    for _ in range(50):
        random.shuffle(current_pool)
        attempt_pairs = []
        possible = True

        for i in range(0, len(current_pool), num_digits):
            digits_chunk = current_pool[i: i + num_digits]

            # ゾロ目チェック(3桁の場合、111などの完全なゾロ目を排除)
            if len(set(digits_chunk)) == 1:
                possible = False
                break

            val = 0
            for d in digits_chunk:
                val = val * 10 + d
            attempt_pairs.append(val)

        if possible:
            return attempt_pairs, True

    return [], False


def apply_signs(temp_terms, minus_count):
    # 最初の項を正、残りの項から指定数をマイナスに設定して計算式を作成
    random.shuffle(temp_terms)
    x1 = temp_terms[0]
    rest = temp_terms[1:]
    minus_indices = random.sample(range(len(rest)), minus_count)
    calc_sequence = [x1] + rest[:]
    for idx in minus_indices:
        calc_sequence[idx + 1] = -calc_sequence[idx + 1]
    return calc_sequence


def has_duplicate_absolute_values(calc_sequence):
    # 数列の絶対値に重複があるかを判定
    absolute_values = [abs(x) for x in calc_sequence]
    return len(absolute_values) != len(set(absolute_values))


def is_cumulative_sum_valid(calc_sequence, num_digits):
    # 累積和が指定範囲内に収まっているかを検証
    min_sum = 10 ** (num_digits - 1)
    max_sum = (10 ** (num_digits + 1)) - 1
    if has_duplicate_absolute_values(calc_sequence):
        return False, 0
    current_sum = 0
    for x in calc_sequence:
        current_sum += x
        if not (min_sum <= current_sum <= max_sum):
            return False, current_sum
    return True, current_sum


def generate_single_problem(num_digits, num_lines, zero_count, minus_count):
    # 指定条件に合致する単一の問題を生成（最大1000回試行）
    digits_pool = create_digits_pool(num_digits, num_lines, zero_count)
    for _ in range(1000):
        current_pool = digits_pool[:]
        random.shuffle(current_pool)
        temp_terms = []
        temp_terms.extend(create_zero_terms(current_pool, zero_count, num_digits))
        non_zero_terms, pairing_success = create_non_zero_terms(current_pool, num_digits)
        if not pairing_success:
            continue
        temp_terms.extend(non_zero_terms)
        calc_sequence = apply_signs(temp_terms, minus_count)
        valid, final_sum = is_cumulative_sum_valid(calc_sequence, num_digits)
        if valid:
            return calc_sequence, final_sum
    return None


def format_formula(terms, ans):
    # 項のリストと答えを「式=答え」の形式にフォーマット
    formula = str(terms[0])
    for num in terms[1:]:
        if num >= 0:
            formula += f"+{num}"
        else:
            formula += f"{num}"
    return f"{formula}={ans}"


def generate_problem_set():
    """
    問題を指定数生成して出力する
    """
    NUM_DIGITS = 2  # 桁数
    NUM_LINES = 8  # 口数
    ZERO_COUNT = 2  # 一の位0の数
    MINUS_COUNT = 3  # マイナスの数
    NUM_QUESTIONS = 5  # 生成する問題数
    TARGET_DIFFICULT_COUNT = 5  # 難(PB+MB以外）の回数

    problems = []
    attempts = 0
    max_attempts = 10000  # 無限ループ防止
    target_pb_mb_count = NUM_DIGITS * NUM_LINES - TARGET_DIFFICULT_COUNT  # PB+MBの回数

    while len(problems) < NUM_QUESTIONS and attempts < max_attempts:
        attempts += 1
        result = generate_single_problem(NUM_DIGITS, NUM_LINES, ZERO_COUNT, MINUS_COUNT)
        if result:
            terms, ans = result
            # ここでPBの数をカウント
            pb_count = count_pb_in_sequence(terms, NUM_DIGITS)
            # MBの数をカウント
            mb_count = count_mb_in_sequence(terms, NUM_DIGITS)
            # P5の数をカウント
            p5_count = count_p5_in_sequence(terms, NUM_DIGITS)
            # M5の数をカウント
            m5_count = count_m5_in_sequence(terms, NUM_DIGITS)
            # P10の数をカウント
            p10_count = count_p10_in_sequence(terms, NUM_DIGITS)
            # M10の数をカウント
            m10_count = count_m10_in_sequence(terms, NUM_DIGITS)
            # P15の数をカウント
            p15_count = count_p15_in_sequence(terms, NUM_DIGITS)
            # M15の数をカウント
            m15_count = count_m15_in_sequence(terms, NUM_DIGITS)

            # PB+MBの合計が目標値と一致する場合のみ追加
            if pb_count + mb_count == target_pb_mb_count:
                problems.append(
                    (terms, ans, pb_count, mb_count, p5_count, m5_count, p10_count, m10_count, p15_count, m15_count))

    print(f"2桁8口を{NUM_QUESTIONS}問 (難:{TARGET_DIFFICULT_COUNT}回のもののみ)")
    for seq, ans, pb, mb, p5, m5, p10, m10, p15, m15 in problems:
        # 出力に回数を追加
        print(f"{format_formula(seq, ans)} ")
        print(f"[M10:{m10}回, M15:{m15}回]")
        print(f"[P10:{p10}回, P15:{p15}回]")
        print(f"[PB:{pb}回, MB:{mb}回, P5:{p5}回, M5:{m5}回]")

    if len(problems) < NUM_QUESTIONS:
        print("指定された条件で十分な問題を生成できませんでした。")


if __name__ == "__main__":
    generate_problem_set()
