import streamlit as st
import random
import io

# 既存のロジックファイルをインポート
from pb_logic import count_pb_in_sequence
from mb_logic import count_mb_in_sequence
from problem_generater import generate_single_problem, format_formula

digit_count = 2 # 2桁

# --- 設定とタイトル ---
st.set_page_config(page_title="計算問題ジェネレーター", layout="centered")
st.title("🧮 2桁問題ジェネレーター")
st.markdown("2桁8口の問題を生成できます")

# --- サイドバー：条件設定 ---
st.sidebar.header("設定")

#digit_count = st.sidebar.number_input("桁数", min_value=1, max_value=2, value=2)
num_lines = st.sidebar.number_input("口数", min_value=3, max_value=15, value=8)
zero_count = st.sidebar.number_input("一の位が0の数", min_value=0, max_value=num_lines, value=2)
minus_count = st.sidebar.number_input("マイナスの数", min_value=0, max_value=num_lines - 1, value=3)
num_questions = st.sidebar.number_input("生成する問題数", min_value=1, max_value=50, value=5)

# 難易度設定（PB+MB以外の回数）
st.sidebar.subheader("難易度調整")
target_difficult_count = st.sidebar.number_input(
    "「難」の数 (PB/MB以外)",
    min_value=0,
    max_value=digit_count * num_lines,
    value=3,
    help="この回数だけPBでもMBでもない計算が含まれます。残りはすべてPBかMBになります。"
)

# 生成ボタン
if st.button("問題を生成する", type="primary"):

    # ターゲットとなるPB+MBの合計回数
    target_pb_mb_count = digit_count * num_lines - target_difficult_count

    if target_pb_mb_count < 0:
        st.error("エラー: 「難」の回数が口数を超えています。")
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
            # (桁数は2で固定としていますが、必要なら変更可)
            result = generate_single_problem(2, num_lines, zero_count, minus_count)

            if result:
                terms, ans = result
                pb = count_pb_in_sequence(terms)
                mb = count_mb_in_sequence(terms)

                # 条件チェック: PB+MBの合計が目標値と一致するか
                if pb + mb == target_pb_mb_count:
                    formatted_q = format_formula(terms, ans)
                    problems.append({
                        "formula": formatted_q,
                        "ans": ans,
                        "pb": pb,
                        "mb": mb,
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

        for i, p in enumerate(problems, 1):
            line_str = f"No.{i}:\n{p['formula']}\n[PB:{p['pb']}, MB:{p['mb']}]"
            st.text(line_str) # 画面表示
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