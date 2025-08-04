from PyQt5.QtWidgets import (
    QMainWindow, QAction, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QInputDialog, QMessageBox, QListWidget, QSplitter, QPushButton,
    QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import Qt

from uuid import UUID

from db.services.game_service import create_game, get_all_games, get_game_by_id, delete_game_by_id
from db.services.card_service import create_card, get_cards_by_game_id, get_cards_by_type, update_card, delete_card


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Microscope AI")
        self.setGeometry(100, 100, 1000, 600)

        self.current_game = None
        self._create_menu()
        self._create_main_layout()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_game_action = QAction("New Game", self)
        new_game_action.triggered.connect(self._create_game)
        file_menu.addAction(new_game_action)

        load_game_action = QAction("Load Game", self)
        load_game_action.triggered.connect(self._enter_game)
        file_menu.addAction(load_game_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _create_main_layout(self):

        # Game Sidebar Info
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()

        self.label_name = QLabel("Game: ")
        self.label_big_picture = QLabel("Big Picture: ")
        self.label_palette_yes = QLabel("Palette (Yes): ")
        self.label_palette_no = QLabel("Palette (No): ")

        self.button_edit_game = QPushButton("Edit Game")
        self.button_delete_game = QPushButton("Delete Game")

        self.button_edit_game.clicked.connect(self._edit_game)
        self.button_delete_game.clicked.connect(self._delete_game)

        for widget in [
            self.label_name, self.label_big_picture,
            self.label_palette_yes, self.label_palette_no,
            self.button_edit_game, self.button_delete_game,
        ]:
            self.sidebar_layout.addWidget(widget)
        self.sidebar.setLayout(self.sidebar_layout)

        # Tree View, Middle
        self.main_tree = QTreeWidget()
        self.main_tree.setColumnCount(1)
        self.main_tree.setHeaderLabel("Story Structure")
        self.main_tree.itemClicked.connect(self._on_tree_click)

        # Card Control Buttons
        self.button_add_period = QPushButton("Add Period")
        self.button_add_event = QPushButton("Add Event")
        self.button_add_scene = QPushButton("Add Scene")

        self.button_add_period.clicked.connect(self._add_period)
        self.button_add_event.clicked.connect(self._add_event)
        self.button_add_scene.clicked.connect(self._add_scene)

        self.card_button_row = QHBoxLayout()
        self.card_button_row.addWidget(self.button_add_period)
        self.card_button_row.addWidget(self.button_add_event)
        self.card_button_row.addWidget(self.button_add_scene)


        self.tree_column = QVBoxLayout()
        self.tree_column.addWidget(self.main_tree)

        button_container = QWidget()
        button_container.setLayout(self.card_button_row)
        self.tree_column.addWidget(button_container)

        tree_widget_container = QWidget()
        tree_widget_container.setLayout(self.tree_column)

        # Card Detail Display
        self.card_text = QTextEdit()
        self.card_text.setReadOnly(True)
        self.card_text.setPlaceholderText("Card Viewer")

        # Main Layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar, 1)
        self.main_layout.addWidget(tree_widget_container, 2)
        self.main_layout.addWidget(self.card_text, 3)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def _create_game(self):
        # TODO Improve error handling (unique game names, etc)
        try:
            name, ok = QInputDialog.getText(self, "Create Game", "Enter game name:")
            if ok and name:
                game = create_game(name)
                self._display_game(game)
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", str(e))

    def _enter_game(self):
        games = get_all_games()
        if not games:
            QMessageBox.information(self, "No Games", "No existing games found.")

        options = [F"{g.name} - {g.id}" for g in games]
        selected, ok = QInputDialog.getItem(self, "Select Game", "Games: ", options, editable=False)
        if ok and selected:
            game_id = selected.split(" - ")[1]
            game = get_game_by_id(UUID(game_id))
            if game:
                self._display_game(game)

    def _display_game(self, game):
        self.current_game = game
        self.label_name.setText(f"Game: {game.name}")
        self.label_big_picture.setText(f"Created: {game.created_at}")
        self.label_palette_yes.setText(f"Palette (Yes): {game.palette_yes or ''}")
        self.label_palette_no.setText(f"Palette (No): {game.palette_no or ''}")

        cards = get_cards_by_game_id(game.id)
        self._build_tree_from_cards(cards)

    def _edit_game(self):
        # TODO - add edit fields and logic
        QMessageBox.information(self, "Edit Game", "< edit functionality to be added >")

    def _delete_game(self):
        if not self.current_game:
            return

        confirm_prompt = QMessageBox.question(
            self, "Delete Game",
            f"Are you sure you want to delete '{self.current_game.name}' and all related cards?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm_prompt == QMessageBox.Yes:
            delete_game_by_id((self.current_game.id))
            self.current_game = None
            self._clear_display()

    def _clear_display(self):
        self.label_name.setText(f"Game: ")
        self.label_big_picture.setText(f"Big Picture: ")
        self.label_palette_yes.setText(f"Palette (Yes): ")
        self.label_palette_no.setText(f"Palette (No): ")
        self.card_text.clear()

    def _on_tree_click(self, item, column):
        card_data = item.data(0, Qt.UserRole)
        if card_data:
            self.card_text.setPlainText(
                f"{card_data['type'].capitalize()}:\n"
                f"Summary: {card_data['summary']}\n\n"
                f"Content: \n{card_data.get('content', '')}"
            )

    def _add_period(self):
        if not self.current_game:
            return

        summary, ok = QInputDialog.getText(self, "Add Period", "Summary:")
        if ok and summary:
            try:
                card = create_card(
                    game_id=self.current_game.id,
                    card_type="period",
                    summary=summary
                )
                self._display_game(self.current_game)
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"Failed to create period:\n{e}")

    def _add_event(self):
        item = self.main_tree.currentItem()
        if not item:
            QMessageBox.warning(self, "No Period Selected", "Select a period to add an event.")
            return

        period_data = item.data(0, Qt.UserRole)
        if period_data.get("type") != "period":
            QMessageBox.warning(self, "Invalid Selection", "Select a period to add an event.")
            return

        summary, ok = QInputDialog.getText(self, "Add Event", "Summary:")
        if ok and summary:
            try:
                card = create_card(
                    game_id=self.current_game.id,
                    card_type='event',
                    summary=summary,
                    period_id=UUID(period_data.get("id"))
                )
                self._display_game(self.current_game)
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"Failed to create event:\n{e}")

    def _add_scene(self):
        item = self.main_tree.currentItem()
        if not item:
            QMessageBox.warning(self, "No Event Selected", "Select an event to add a scene.")
            return

        event_data = item.data(0, Qt.UserRole)
        if event_data.get("type") != "event":
            QMessageBox.warning(self, "Invalid Selection", "Select an event to add a scene.")
            return

        summary, ok = QInputDialog.getText(self, "Add Scene", "Summary:")
        if ok and summary:
            try:
                card = create_card(
                    game_id=self.current_game.id,
                    card_type='scene',
                    summary=summary,
                    event_id=UUID(event_data.get("id"))
                )
                self._display_game(self.current_game)
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"Failed to create scene:\n{e}")

    def _build_tree_from_cards(self, cards):
        self.main_tree.clear()

        period_map = {}
        event_map = {}

        for card in cards:
            card_data = {
                "id": str(card.id),
                "type": card.type,
                "summary": card.summary,
                "content": card.content or ""
            }

            item = QTreeWidgetItem()

            if card.type == "period":
                item.setText(0, "PERIOD: " + card.summary)
                item.setData(0, Qt.UserRole, card_data)
                self.main_tree.addTopLevelItem(item)
                period_map[card.id] = item

            elif card.type == "event" and card.period_id in period_map:
                item.setText(0, "EVENT: " + card.summary)
                item.setData(0, Qt.UserRole, card_data)
                period_map[card.period_id].addChild(item)
                event_map[card.id] = item

            elif card.type == "scene" and card.event_id in event_map:
                item.setText(0, "SCENE: " + card.summary)
                item.setData(0, Qt.UserRole, card_data)
                event_map[card.event_id].addChild(item)

            self.main_tree.expandAll()