class BetInputManager:
    def __init__(self, bet_processor, turn_manager, input_handler):
        # Recebe as dependências necessárias para processar a aposta
        self.bet_processor = bet_processor
        self.turn_manager = turn_manager
        self.input_handler = input_handler
        
        # Estado interno da aposta
        self.is_active = False
        self.current_text = ""
        self.selected_type = None
        self.selected_target = None
        self.last_message = "Bem-vindo ao Probabilidado!"

    def prepare_bet(self, cell_value, row, col):
        # Configura o tipo de aposta com base no valor da célula clicada
        if cell_value == 4:
            self.selected_type = 'quadrant'
            self.selected_target = row
            self.is_active = True
        elif cell_value in (5, 6, 7):
            self.selected_type = 'color'
            self.selected_target = cell_value
            self.is_active = True
        elif cell_value in (1, 2, 3):
            self.selected_type = 'ordered_pair'
            self.selected_target = (row, col)
            self.is_active = True

    def process_keystroke(self, event):
        # Trata o texto digitado
        if event.key == pygame.K_RETURN:
            self._execute()
        else:
            self.current_text = self.input_handler.handle_keyboard_input(event, self.current_text)

    def _execute(self):
        # Tenta executar a aposta e atualiza a mensagem
        if not self.current_text.isdigit():
            self.last_message = "Valor de aposta inválido."
            self.reset_state()
            return

        bet_amount = int(self.current_text)
        current_player = self.turn_manager.get_current_player()
        
        success, message = self.bet_processor.process_bet(
            current_player, self.selected_type, bet_amount, self.selected_target
        )
        
        self.last_message = message
        if success:
            self.turn_manager.advance_turn()
            
        self.reset_state()

    def reset_state(self):
        # Limpa os campos após a aposta
        self.is_active = False
        self.current_text = ""
        self.selected_type = None
        self.selected_target = None