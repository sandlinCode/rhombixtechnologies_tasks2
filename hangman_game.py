import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt


class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎀 Cute Hangman Game 🎀")
        self.setFixedSize(600, 500)

        # --- Colors and Style ---
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#FFF8F2"))  # Soft ivory background
        self.setPalette(palette)

        self.words = [
            "python", "developer", "hangman", "challenge",
            "computer", "artificial", "intelligence", "keyboard"
        ]
        self.reset_game()

        # --- Layouts ---
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Title Label
        self.title_label = QLabel("🎮 Welcome to Hangman!")
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #FF7BAC;")
        main_layout.addWidget(self.title_label)

        # Word Display
        self.word_label = QLabel(self.get_display_word())
        self.word_label.setFont(QFont("Consolas", 24, QFont.Bold))
        self.word_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.word_label)

        # Attempts Counter
        self.attempts_label = QLabel(f"Attempts left: {self.attempts}")
        self.attempts_label.setFont(QFont("Segoe UI", 14))
        self.attempts_label.setAlignment(Qt.AlignCenter)
        self.attempts_label.setStyleSheet("color: #555;")
        main_layout.addWidget(self.attempts_label)

        # Letter Buttons (A–Z)
        grid = QGridLayout()
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            btn = QPushButton(letter)
            btn.setFixedSize(45, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFD6E0;
                    border: none;
                    border-radius: 10px;
                    color: #333;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FFB6C1;
                }
                QPushButton:disabled {
                    background-color: #F5F5F5;
                    color: #AAA;
                }
            """)
            btn.clicked.connect(lambda _, l=letter: self.guess_letter(l.lower()))
            grid.addWidget(btn, i // 9, i % 9)
        main_layout.addLayout(grid)

        # Restart Button
        self.restart_btn = QPushButton("🔄 Restart Game")
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFB6C1;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 14px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF9BB2;
            }
        """)
        self.restart_btn.clicked.connect(self.reset_ui)
        main_layout.addWidget(self.restart_btn)

        self.setLayout(main_layout)

    def reset_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = []
        self.attempts = 6

    def get_display_word(self):
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.append(letter)

        if letter not in self.word:
            self.attempts -= 1

        self.word_label.setText(self.get_display_word())
        self.attempts_label.setText(f"Attempts left: {self.attempts}")

        if all(l in self.guessed_letters for l in self.word):
            QMessageBox.information(self, "🎉 You Win!", f"You guessed the word: {self.word}")
            self.disable_all_buttons()
        elif self.attempts == 0:
            QMessageBox.warning(self, "💀 Game Over", f"The word was: {self.word}")
            self.disable_all_buttons()

        # Disable clicked button
        for btn in self.findChildren(QPushButton):
            if btn.text().lower() == letter:
                btn.setDisabled(True)

    def disable_all_buttons(self):
        for btn in self.findChildren(QPushButton):
            if btn.text().isalpha():
                btn.setDisabled(True)

    def reset_ui(self):
        self.reset_game()
        self.word_label.setText(self.get_display_word())
        self.attempts_label.setText(f"Attempts left: {self.attempts}")
        for btn in self.findChildren(QPushButton):
            if btn.text().isalpha():
                btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HangmanGame()
    window.show()
    sys.exit(app.exec_())
