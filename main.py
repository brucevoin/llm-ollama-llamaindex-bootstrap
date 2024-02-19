"""
Description: 
Author: haichun feng
Date: 2024-02-18 11:18:32
LastEditor: haichun feng
LastEditTime: 2024-02-18 11:51:25
"""

from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import input_dialog
import os
from ingest import ingest_data
from rag.pipeline import build_rag_pipeline
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

rag_chain = build_rag_pipeline()


def main():
    session = PromptSession()
    completer = WordCompleter(["ingest", "chat"])
    while True:
        try:
            text = session.prompt(
                "Please type command(ingest|chat):", completer=completer
            )
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if text == "ingest":
                ingest()
            elif text == "chat":
                chat()
            else:
                print("error\n")
    print("GoodBye!")


def chat():
    session = PromptSession()
    while True:
        try:
            prompt = session.prompt("please input prompt> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if prompt is not None:
                print('Retrieving answer...')
                try:
                    answer = rag_chain.query(prompt)
                    answer = str(answer).strip()
                    print('\n' + answer + '\n')
                except ConnectionError:
                    print('\nConnectionError')
                continue
            else:
                continue


def ingest():
    session = PromptSession()
    try:
        text = input_dialog(
            title="Select file", text="Please type your documents folder path:"
        ).run()

        if text is None:
            return
    except KeyboardInterrupt:
        return
    except EOFError:
        return
    else:
        if os.path.isdir(text):
            ingest_data(text)
        else:
            print("The folder does not exist.")


if __name__ == "__main__":
    main()
