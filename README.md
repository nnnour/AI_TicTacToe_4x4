# 🧠 Tic-Tac-Toe AI 🤖

Welcome to **Tic-Tac-Toe AI** – the ultimate 4x4 twist on the classic game! Whether you're here to outsmart an AI opponent or just enjoy the thrill of strategic play, this game is packed with fun and challenges for everyone! This game was created for my CS152 AI class! 🎮✨

## ✨ Features ✨

- **Three Unique Difficulty Levels**:
  - 😅 **Easy**: A delightful mix of AI logic and randomized moves for unpredictable fun! 🎲
  - 🧠 **Medium**: Powered by **Minimax with Alpha-Beta Pruning**, offering a balanced challenge to test your strategic skills! 💡
  - 🤖 **Hard**: Goes full throttle with **Minimax and Alpha-Beta Pruning**, ensuring optimal decision-making. 🏆
- **4x4 Gameplay**: A strategic upgrade from the classic 3x3 board. Think ahead, plan smarter! 🔢
- **Performance Tracking**: Visualize the AI's efficiency with an interactive **performance plot**. 📊

## 🎨 What's Under the Hood?

### AI Logic:
- **Minimax with Alpha-Beta Pruning**:
  - Used in different modes for optimal decision-making and efficient tree traversal. 🤓
  - Depth of the search tree varies by difficulty level:
    - Easy: Low depth randomized moves and simplified AI logic to keep the game light-hearted and fun. 🎲 
    - Medium: Moderate depth for a balanced challenge. 🧠
    - Hard: Maximum depth for strategic perfection. 🤖

### Interactive Plots:
- Use the **Plot Performance** button to track the AI's decision-making.
- The graph shows how many nodes were evaluated during gameplay, giving you insight into the AI's thought process. 📈

## 🚀 How to Play

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/AI_TicTacToe_4x4.git
   cd AI_TicTacToe_4x4
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the game:
   ```bash
   python3 main.py
   ```

Enjoy strategizing and defeating the AI (or maybe being humbled by its brilliance)! 🎉
