from typing import List, Optional, Dict, Tuple, Set, Any
import copy
import random
from enum import Enum
import importlib.util
from datetime import datetime

from .models import WordConnectionsState, WordConnectionsMove, WordCell, GameSource
from src.haive.games.framework.base import GameStateManager

# Try to import selenium components for NYT scraping
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Try to import playwright as an alternative
try:
    import playwright
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class WordConnectionsStateManager(GameStateManager[WordConnectionsState]):
    """Manager for Word Connections game state."""
    
    # Sample categories and word sets for the game
    SAMPLE_CATEGORIES = {
        "Colors": ["RED", "BLUE", "GREEN", "YELLOW"],
        "Fruits": ["APPLE", "ORANGE", "BANANA", "GRAPE"],
        "Animals": ["LION", "TIGER", "BEAR", "WOLF"],
        "Countries": ["FRANCE", "SPAIN", "ITALY", "GERMANY"],
        "Vehicles": ["CAR", "TRUCK", "BUS", "TRAIN"],
        "Sports": ["SOCCER", "TENNIS", "GOLF", "BASEBALL"],
        "Planets": ["MARS", "VENUS", "JUPITER", "SATURN"],
        "Tools": ["HAMMER", "SAW", "DRILL", "WRENCH"],
        "Flowers": ["ROSE", "DAISY", "TULIP", "LILY"],
        "Instruments": ["PIANO", "GUITAR", "VIOLIN", "DRUMS"],
        "Clothing": ["SHIRT", "PANTS", "SHOES", "HAT"],
        "Weather": ["RAIN", "SNOW", "WIND", "STORM"],
        "Elements": ["WATER", "FIRE", "EARTH", "AIR"],
        "Body Parts": ["HEAD", "HAND", "FOOT", "EYE"],
        "Furniture": ["CHAIR", "TABLE", "DESK", "BED"],
        "Greek Letters": ["ALPHA", "BETA", "DELTA", "GAMMA"],
        "Metals": ["GOLD", "SILVER", "COPPER", "IRON"],
        "Emotions": ["HAPPY", "SAD", "ANGRY", "SCARED"],
        "Trees": ["OAK", "PINE", "MAPLE", "BIRCH"],
        "Directions": ["NORTH", "SOUTH", "EAST", "WEST"],
        "Desserts": ["CAKE", "PIE", "COOKIE", "BROWNIE"],
        "Seasons": ["SPRING", "SUMMER", "FALL", "WINTER"],
        "Celestial Bodies": ["SUN", "MOON", "STAR", "COMET"],
        "Occupations": ["DOCTOR", "TEACHER", "ENGINEER", "ARTIST"],
        "Game Pieces": ["PAWN", "KNIGHT", "BISHOP", "ROOK"],
        "Card Suits": ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
    }
    
    # More complex and interesting categories for variety
    ADVANCED_CATEGORIES = {
        "Things with Shells": ["TURTLE", "EGG", "PEANUT", "TACO"],
        "Things with Keys": ["PIANO", "DOOR", "MAP", "KEYBOARD"],
        "Parts of a Book": ["INDEX", "COVER", "SPINE", "CHAPTER"],
        "Things That Are Drained": ["BATTERY", "PASTA", "SINK", "ENERGY"],
        "Words with Double Letters": ["BOOK", "DOOR", "SHEET", "MILLION"],
        "Units of Time": ["SECOND", "MINUTE", "HOUR", "YEAR"],
        "Computer Terms": ["MOUSE", "WINDOW", "MEMORY", "DISK"],
        "Olympic Sports": ["BOXING", "ROWING", "DIVING", "ARCHERY"]
    }
    
    # Combine all categories
    ALL_CATEGORIES = {**SAMPLE_CATEGORIES, **ADVANCED_CATEGORIES}
    
    DIFFICULTY_LEVELS = ["yellow", "green", "blue", "purple"]
    
    @classmethod
    def initialize(cls, source: str = "internal", **kwargs) -> WordConnectionsState:
        """Initialize a new Word Connections game.
        
        Args:
            source: Source of the game data ('internal' or 'nyt')
            **kwargs: Additional options for game creation
        
        Returns:
            WordConnectionsState: The initialized game state
        """
        if source.lower() == "nyt" and (SELENIUM_AVAILABLE or PLAYWRIGHT_AVAILABLE):
            try:
                return cls._initialize_from_nyt(**kwargs)
            except Exception as e:
                print(f"Error fetching NYT Connections: {e}")
                print("Falling back to internal categories")
                # Fall back to internal if NYT scraping fails
                return cls._initialize_internal(**kwargs)
        else:
            return cls._initialize_internal(**kwargs)
    
    @classmethod
    def _initialize_internal(cls, **kwargs) -> WordConnectionsState:
        """Initialize a game with internal categories."""
        # Get categories to use
        categories_to_use = cls.ALL_CATEGORIES
        
        # Select specific categories if provided
        selected_category_names = kwargs.get("categories", None)
        if selected_category_names:
            # Use only the specified categories
            categories = {}
            for name in selected_category_names:
                if name in categories_to_use:
                    categories[name] = categories_to_use[name]
                    
            # If not enough categories were found, add random ones
            if len(categories) < 4:
                remaining = 4 - len(categories)
                available = [k for k in categories_to_use.keys() if k not in categories]
                if available:
                    additional = random.sample(available, min(remaining, len(available)))
                    for name in additional:
                        categories[name] = categories_to_use[name]
        else:
            # Select 4 random categories
            all_categories = list(categories_to_use.keys())
            selected_categories = random.sample(all_categories, 4)
            
            # Create the categories dict with selected categories
            categories = {}
            for category in selected_categories:
                categories[category] = categories_to_use[category]
        
        # Assign difficulty levels
        category_difficulty = {}
        category_list = list(categories.keys())
        random.shuffle(category_list)  # Randomize order for difficulty assignment
        for i, category in enumerate(category_list):
            category_difficulty[category] = cls.DIFFICULTY_LEVELS[i]
        
        # Create the grid of cells
        cell_words = []
        for words in categories.values():
            cell_words.extend(words)
            
        # Shuffle the grid
        random.shuffle(cell_words)
        
        # Create cell objects
        cells = []
        for i, word in enumerate(cell_words):
            cells.append(WordCell(
                word=word,
                index=i,
                selected=False,
                solved=False
            ))
        
        # Create and return the initial state
        return WordConnectionsState(
            cells=cells,
            remaining_words=[cell.word for cell in cells],
            discovered_groups={},
            incorrect_attempts=[],
            attempts_remaining=4,
            categories=categories,
            category_difficulty=category_difficulty,
            game_source=GameSource.INTERNAL,
            turn="player",
            game_status="ongoing",
            move_history=[],
            score=0
        )
    
    @classmethod
    def _initialize_from_nyt(cls, **kwargs) -> WordConnectionsState:
        """Initialize a game by scraping the NYT Connections game."""
        # Use either Selenium or Playwright to scrape NYT Connections
        if SELENIUM_AVAILABLE:
            return cls._scrape_nyt_with_selenium(**kwargs)
        elif PLAYWRIGHT_AVAILABLE:
            return cls._scrape_nyt_with_playwright(**kwargs)
        else:
            raise ImportError("Neither Selenium nor Playwright is available")
            
    @classmethod
    def _scrape_nyt_with_selenium(cls, **kwargs) -> WordConnectionsState:
        """Scrape NYT Connections using Selenium."""
        print("Scraping NYT Connections with Selenium...")
        
        # Setup Chrome options for headless operation
        chrome_options = Options()
        if not kwargs.get("visible", False):
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Initialize the browser
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        try:
            # Navigate to the NYT Connections page
            driver.get("https://www.nytimes.com/games/connections")
            
            # Accept cookies if prompt appears
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-3fhaqb"))
                ).click()
            except:
                # Cookie prompt might not appear
                pass
            
            # Click play button
            try:
                play_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.primary-button"))
                )
                play_button.click()
            except Exception as e:
                print(f"Error clicking play button: {e}")
                
            # Wait for game board to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.game-wrapper"))
            )
            
            # Extract words from the grid
            word_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item-content"))
            )
            
            words = [element.text.strip().upper() for element in word_elements]
            if len(words) != 16:
                raise ValueError(f"Expected 16 words, found {len(words)}")
            
            # We can't directly get the categories from NYT until they're discovered
            # So we'll create placeholder categories for now
            categories = {
                "Category 1": words[0:4],
                "Category 2": words[4:8],
                "Category 3": words[8:12],
                "Category 4": words[12:16],
            }
            
            # Assign difficulty levels
            category_difficulty = {}
            for i, category in enumerate(categories.keys()):
                category_difficulty[category] = cls.DIFFICULTY_LEVELS[i]
            
            # Create cell objects
            cells = []
            for i, word in enumerate(words):
                cells.append(WordCell(
                    word=word,
                    index=i,
                    selected=False,
                    solved=False
                ))
            
            # Get the current date for the game
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Create and return the initial state
            return WordConnectionsState(
                cells=cells,
                remaining_words=[cell.word for cell in cells],
                discovered_groups={},
                incorrect_attempts=[],
                attempts_remaining=4,
                categories=categories,  # These are placeholders
                category_difficulty=category_difficulty,
                game_source=GameSource.NYT,
                game_date=today,
                turn="player",
                game_status="ongoing",
                move_history=[],
                score=0
            )
        finally:
            # Close the browser
            driver.quit()
    
    @classmethod
    def _scrape_nyt_with_playwright(cls, **kwargs) -> WordConnectionsState:
        """Scrape NYT Connections using Playwright."""
        print("Scraping NYT Connections with Playwright...")
        
        with sync_playwright() as p:
            # Launch browser (headless by default)
            browser_type = kwargs.get("browser", "chromium")
            headless = not kwargs.get("visible", False)
            
            if browser_type == "firefox":
                browser = p.firefox.launch(headless=headless)
            elif browser_type == "webkit":
                browser = p.webkit.launch(headless=headless)
            else:
                browser = p.chromium.launch(headless=headless)
                
            # Create a new page
            page = browser.new_page()
            page.set_default_timeout(30000)  # 30 seconds timeout
            
            try:
                # Navigate to NYT Connections
                page.goto("https://www.nytimes.com/games/connections")
                
                # Accept cookies if prompt appears
                try:
                    page.click("button.css-3fhaqb", timeout=5000)
                except:
                    # Cookie prompt might not appear
                    pass
                
                # Click play button
                try:
                    page.click("button:has-text('Play')", timeout=10000)
                except:
                    # Try alternative play button selector
                    try:
                        page.click("button:has-text('Continue')", timeout=10000)
                    except:
                        try:
                            page.click("button.primary-button", timeout=10000)
                        except Exception as e:
                            print("No play button found")
                            print(f"Error clicking play button: {e}")
                
                # Wait for game board to load
                page.wait_for_selector("div.game-wrapper", timeout=10000)
                
                # Extract words from the grid
                word_elements = page.query_selector_all("div.item-content")
                words = [element.inner_text().strip().upper() for element in word_elements]
                
                if len(words) != 16:
                    raise ValueError(f"Expected 16 words, found {len(words)}")
                
                # Create placeholder categories
                categories = {
                    "Category 1": words[0:4],
                    "Category 2": words[4:8],
                    "Category 3": words[8:12],
                    "Category 4": words[12:16],
                }
                
                # Assign difficulty levels
                category_difficulty = {}
                for i, category in enumerate(categories.keys()):
                    category_difficulty[category] = cls.DIFFICULTY_LEVELS[i]
                
                # Create cell objects
                cells = []
                for i, word in enumerate(words):
                    cells.append(WordCell(
                        word=word,
                        index=i,
                        selected=False,
                        solved=False
                    ))
                
                # Get the current date for the game
                today = datetime.now().strftime("%Y-%m-%d")
                
                # Create and return the initial state
                return WordConnectionsState(
                    cells=cells,
                    remaining_words=[cell.word for cell in cells],
                    discovered_groups={},
                    incorrect_attempts=[],
                    attempts_remaining=4,
                    categories=categories,  # These are placeholders
                    category_difficulty=category_difficulty,
                    game_source=GameSource.NYT,
                    game_date=today,
                    turn="player",
                    game_status="ongoing",
                    move_history=[],
                    score=0
                )
            finally:
                # Close the browser
                browser.close()
    
    @classmethod
    def apply_move(cls, state: WordConnectionsState, move: WordConnectionsMove) -> WordConnectionsState:
        """Apply a move to the Word Connections state."""
        # Create a deep copy of the state to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Extract words from the move
        selected_words = move.words
        
        # Parse indices if provided, otherwise find them
        if move.indices and len(move.indices) == 4:
            selected_indices = move.indices
        else:
            # Find indices for the selected words
            selected_indices = []
            for word in selected_words:
                for i, cell in enumerate(new_state.cells):
                    if cell.word == word and not cell.solved:
                        selected_indices.append(i)
                        break
                        
        # Validate the move
        if len(selected_indices) != 4:
            new_state.error_message = f"Invalid move: Could not find all 4 words on the grid or some are already solved."
            return new_state
            
        # Check if these 4 words constitute a valid category
        # Find which category (if any) these words belong to
        selected_word_set = set(selected_words)
        matching_category = None
        for category, category_words in new_state.categories.items():
            if selected_word_set == set(category_words):
                matching_category = category
                break
                
        # Update move with result
        move.result = "correct" if matching_category else "incorrect"
        
        # Update move history
        new_state.move_history.append(move)
        
        # Process result based on whether it's a correct grouping
        if matching_category:
            # Correct grouping!
            # Add to discovered groups
            new_state.discovered_groups[matching_category] = selected_words
            
            # Mark cells as solved
            for i in selected_indices:
                new_state.cells[i].solved = True
                new_state.cells[i].category = matching_category
                if new_state.cells[i].word in new_state.remaining_words:
                    new_state.remaining_words.remove(new_state.cells[i].word)
            
            # Clear selection
            new_state.selected_indices = []
            
            # Update player score
            new_state.score += 1
        else:
            # Incorrect grouping
            new_state.incorrect_attempts.append(selected_words)
            new_state.attempts_remaining -= 1
            new_state.incorrect_submissions += 1
            
        # Check for game over conditions
        new_state = cls.check_game_status(new_state)
        
        return new_state
    
    @classmethod
    def select_cell(cls, state: WordConnectionsState, cell_index: int) -> WordConnectionsState:
        """Toggle selection of a cell."""
        # Create a deep copy of the state to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Validate cell index
        if cell_index < 0 or cell_index >= len(new_state.cells):
            new_state.error_message = f"Invalid cell index: {cell_index}"
            return new_state
            
        # Check if cell is already solved
        if new_state.cells[cell_index].solved:
            new_state.error_message = f"Cell {cell_index} is already solved"
            return new_state
            
        # Toggle selection
        if cell_index in new_state.selected_indices:
            # Deselect
            new_state.selected_indices.remove(cell_index)
            new_state.cells[cell_index].selected = False
        else:
            # Can only select if we have fewer than 4 selections
            if len(new_state.selected_indices) >= 4:
                new_state.error_message = "Cannot select more than 4 cells"
                return new_state
                
            # Select
            new_state.selected_indices.append(cell_index)
            new_state.cells[cell_index].selected = True
            
        return new_state
    
    @classmethod
    def submit_selection(cls, state: WordConnectionsState) -> WordConnectionsState:
        """Submit the current selection as a move."""
        # Create a deep copy of the state to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Check if exactly 4 cells are selected
        if len(new_state.selected_indices) != 4:
            new_state.error_message = f"Must select exactly 4 cells, selected {len(new_state.selected_indices)}"
            return new_state
            
        # Get words from selected cells
        selected_words = [new_state.cells[i].word for i in new_state.selected_indices]
        
        # Create a move
        move = WordConnectionsMove(
            words=selected_words,
            indices=new_state.selected_indices.copy()
        )
        
        # Apply the move
        return cls.apply_move(new_state, move)
    
    @classmethod
    def get_legal_moves(cls, state: WordConnectionsState) -> List[WordConnectionsMove]:
        """Get all legal moves for the current state."""
        # In a single-player game, legal moves are any combinations of 4 unsolved words
        # Since there would be too many combinations, we'll return a few smart guesses
        
        # Find all unsolved cells
        unsolved_cells = [cell for cell in state.cells if not cell.solved]
        
        # If fewer than 4 cells remain, no legal moves
        if len(unsolved_cells) < 4:
            return []
            
        # Extract just the first legal move (for LLM to extend)
        if len(unsolved_cells) >= 4:
            words = [cell.word for cell in unsolved_cells[:4]]
            indices = [cell.index for cell in unsolved_cells[:4]]
            return [WordConnectionsMove(words=words, indices=indices)]
            
        return []
    
    @classmethod
    def check_game_status(cls, state: WordConnectionsState) -> WordConnectionsState:
        """Check and update game status."""
        # Check if all categories have been discovered
        if len(state.discovered_groups) == len(state.categories):
            # Game complete - victory!
            state.game_status = "victory"
                
        # Check if out of attempts
        elif state.attempts_remaining <= 0:
            state.game_status = "defeat"
                
        return state