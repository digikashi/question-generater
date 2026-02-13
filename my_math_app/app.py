import streamlit as st
import random
import io

# 既存のロジックファイルをインポート
from pb_logic import count_pb_in_sequence
from mb_logic import count_mb_in_sequence
from p5_logic import count_p5_in_sequence
from p10_logic import count_p10_in_sequence
from p15_logic import count_p15_in_sequence
from m5_logic import count_m5_in_sequence
from m10_logic import count_m10_in_sequence
from m15_logic import count_m15_in_sequence
from problem_generater import generate_single_problem, format_formula

# --- 設定とタイトル ---
st.set_page_config(page_title="計算問題ジェネレーター", layout="centered")
st.title("🧮 問題ジェネレーター")
st.markdown("条件を指定して問題を生成できます")

# --- サイドバー：条件設定 ---
st.sidebar.header("設定")

digit_count = 2
# digit_count = st.sidebar.number_input("桁数", min_value=1, max_value=4, value=2)
num_lines = st.sidebar.number_input("口数", min_value=1, max_value=15, value=8)
zero_count = st.sidebar.number_input("0の数", min_value=0, max_value=15, value=2)
minus_count = st.sidebar.number_input("マイナスの数", min_value=0, max_value=14, value=3)
num_questions = st.sidebar.number_input("生成する問題数", min_value=1, max_value=50, value=5)

st.sidebar.divider()
st.sidebar.subheader("難易度調整")

target_p5_count = st.sidebar.number_input("P5", min_value=0, max_value=digit_count * num_lines, value=1)
target_p10_count = st.sidebar.number_input("P10", min_value=0, max_value=digit_count * num_lines, value=1)
target_p15_count = st.sidebar.number_input("P15", min_value=0, max_value=digit_count * num_lines, value=1)
target_m5_count = st.sidebar.number_input("M5", min_value=0, max_value=digit_count * num_lines, value=1)
target_m10_count = st.sidebar.number_input("M10", min_value=0, max_value=digit_count * num_lines, value=1)
target_m15_count = st.sidebar.number_input("M15", min_value=0, max_value=digit_count * num_lines, value=1)

total_difficult = target_p5_count + target_p10_count + target_p15_count + target_m5_count + target_m10_count + target_m15_count
st.sidebar.text(f"「難」の合計: {total_difficult} 回")

# 生成ボタン
if st.button("問題を生成する", type="primary"):

    if minus_count >= num_lines:
        st.error("エラー: マイナスの回数が口数以上です。")
    elif digit_count == 2 and zero_count > num_lines:
        st.error("エラー: 0の回数が口数を超えています。")
    else:
        problems = []
        attempts = 0
        max_attempts = 20000  # ループ回数制限

        progress_bar = st.progress(0)
        status_text = st.empty()

        # --- 生成ループ ---
        while len(problems) < num_questions and attempts < max_attempts:
            attempts += 1

            # 既存の関数を利用して単一問題を生成
            result = generate_single_problem(digit_count, num_lines, zero_count, minus_count)

            if result:
                terms, ans = result

                # もしp5が一致しなければ、他の計算をする前にスキップしたほうが高速
                p5 = count_p5_in_sequence(terms, digit_count)
                if p5 != target_p5_count:
                    continue

                p10 = count_p10_in_sequence(terms, digit_count)
                if p10 != target_p10_count:
                    continue

                p15 = count_p15_in_sequence(terms, digit_count)
                if p15 != target_p15_count:
                    continue

                m5 = count_m5_in_sequence(terms, digit_count)
                if m5 != target_m5_count:
                    continue

                m10 = count_m10_in_sequence(terms, digit_count)
                if m10 != target_m10_count:
                    continue

                m15 = count_m15_in_sequence(terms, digit_count)
                if m15 != target_m15_count:
                    continue

                pb = count_pb_in_sequence(terms)
                mb = count_mb_in_sequence(terms)

                formatted_q = format_formula(terms, ans)
                problems.append({
                    "formula": formatted_q,
                    "ans": ans,
                    "pb": pb,
                    "mb": mb,
                    "p5": p5,
                    "p10": p10,
                    "p15": p15,
                    "m5": m5,
                    "m10": m10,
                    "m15": m15,
                    "terms": terms
                })

                # 進捗バー更新
                progress_bar.progress(len(problems) / num_questions)

        status_text.empty()
        progress_bar.empty()

        # --- 結果表示 ---
        if len(problems) < num_questions:
            st.warning(f"{len(problems)}問しか生成できませんでした。条件が厳しい可能性があります。")
        else:
            st.success(f"{len(problems)}問の生成に成功しました！")

        # テキストデータ作成（コピー用・ダウンロード用）
        output_text = ""
        st.subheader("生成結果")
        # ユーザーが指定した「目標値」を表示するのが自然です
        # ユーザーが指定した「目標値」を表示（全角スペースを削除し、半角スペース4つに修正）
        st.text(
            f"条件設定 -> P5: {target_p5_count}回, P10: {target_p10_count}回, P15: {target_p15_count}回, M5: {target_m5_count}回, M10: {target_m10_count}回, M15: {target_m15_count}回")

        for i, p in enumerate(problems, 1):
            line_str = f"No.{i}:\n{p['formula']}\n"
            st.text(line_str)  # 画面表示
            output_text += line_str + "\n"

        # ダウンロードボタン
        st.download_button(
            label="テキストファイルとしてダウンロード",
            data=output_text,
            file_name="math_problems.txt",
            mime="text/plain"
        )

        # 詳細表示（アコーディオン）
        with st.expander("詳細データ（縦書き用データなど）を見る"):
            st.write(problems)
