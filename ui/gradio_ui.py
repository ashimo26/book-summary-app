# ui/gradio_ui.py
import gradio as gr
from loaders.pdf_loader import add_pdf_to_vectorstore
from chains.qa_chain import answer_question, delete_doc
from quiz.quiz_generator import generate_quiz_question, check_answer
import os

# チャット履歴を保持
chat_history = []

def qa_chat(user_question, history, doc_id):
    answer = answer_question(user_question, doc_id)
    history.append([user_question, answer])
    return history, ""

def get_folder_options():
    return [d for d in os.listdir("chroma_store") if os.path.isdir(os.path.join("chroma_store", d))]

def create_ui():
    with gr.Blocks() as demo:
        with gr.Tab("ファイルアップロード"):
            gr.Markdown("### PDFファイルをアップロードしてベクトルストアに読み込ませる")
            file_input = gr.File(label="PDFを選択", file_types=[".pdf"])
            upload_btn = gr.Button("アップロード")
            upload_output = gr.Textbox(label="アップロード結果")
            upload_status = gr.Textbox(lines=1, interactive=False)
            upload_btn.click(fn=add_pdf_to_vectorstore, inputs=file_input, outputs=upload_status, queue=True)

        with gr.Tab("Q&A"):
            gr.Markdown("### 文書に基づいてGPTに質問できます")
            folder_options = get_folder_options()
            folder_dropdown = gr.Dropdown(choices=folder_options, label="選択するフォルダ")
            chatbot = gr.Chatbot(label="Q&A Chatbot")
            question_box = gr.Textbox(label="質問を入力")
            ask_btn = gr.Button("質問する")
            ask_btn.click(fn=qa_chat, inputs=[question_box, chatbot, folder_dropdown], outputs=[chatbot, question_box])

            # 削除結果を表示するための一時的なメッセージを設定
            def update_delete_status(doc_id):
                result = delete_doc(doc_id)
                # フォルダの選択肢を再取得
                updated_folders = get_folder_options()
                gr.Info(result)
                return gr.update(choices=updated_folders)
            
            delete_btn = gr.Button("削除する")
            delete_btn.click(fn=update_delete_status, inputs=[folder_dropdown], outputs=[folder_dropdown])

        with gr.Tab("復習モード"):
            gr.Markdown("### 文書内容に関する四択クイズに挑戦しましょう")
            quiz_question = gr.Markdown("", label="質問文")
            quiz_options = gr.Radio([], label="選択肢")
            generate_btn = gr.Button("新しい問題を生成")
            answer_btn = gr.Button("解答する")
            feedback = gr.Textbox(label="フィードバック")
            generate_btn.click(fn=generate_quiz_question, inputs=None, outputs=[quiz_question, quiz_options])
            answer_btn.click(fn=check_answer, inputs=quiz_options, outputs=feedback)

    return demo