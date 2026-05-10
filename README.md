# Probabilidado 🎲

**Probabilidado** é um jogo educativo e interativo desenvolvido em Python com a biblioteca Pygame. O projeto combina conceitos de probabilidade com uma interface moderna e modularizada, focado em proporcionar uma experiência de usuário fluida e atrativa.

## 📝 Sobre o Projeto
O jogo desafia dois jogadores a apostarem suas fichas em resultados de lançamentos de dados. Os jogadores podem apostar em cores, quadrantes específicos ou até no par ordenado exato resultante do lançamento. O objetivo é terminar as 5 rodadas com o maior número de fichas ou levar o oponente à falência.

## 🚀 Funcionalidades
- **Sistema de Apostas Variado:** Apostas em Quadrantes (3x), Cores (1x a 4x) ou Par Ordenado Exato (5x).
- **Gerenciamento de Estado:** Controle automático de turnos, rodadas e saldo de fichas.
- **Interface Moderna (Dashboard):** Painel lateral organizado com informações em tempo real, cards de status e efeitos de sombra/arredondamento.
- **Feedback Sonoro:** Efeitos sonoros para lançamentos de dados, vitórias e erros.
- **Validações:** Limites de caracteres para nomes (12) e apostas (3 dígitos), além de verificação de saldo.
- **Morte Súbita:** O jogo termina imediatamente se um jogador ficar sem fichas.

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **Pygame:** Para renderização gráfica e manipulação de eventos.
- **Arquitetura Modular:** Separação clara entre Modelos (Models) e Controladores (Controllers).

## 📂 Estrutura do Projeto
O projeto segue uma estrutura organizada para facilitar a manutenção:

- `main.py`: Ponto de entrada que gerencia o loop principal e eventos.
- `config.py`: Centralização de constantes, cores, fontes e configurações globais.
- **controllers/**
  - `game_controller.py`: Orquestrador principal do estado do jogo.
  - `bets_controller.py`: Lógica específica para processamento e validação de apostas.
  - `restart_controller.py`: Gerenciamento do reinício da partida.
- **models/**
  - `player.py`: Entidade que representa o jogador e seu saldo.
  - `scene.py`: Responsável pela renderização do tabuleiro e detecção de cliques.
- **assets/sounds/**: Arquivos de áudio `.wav`.

## 🎮 Como Jogar
1. **Instalação:** Certifique-se de ter o Python e o Pygame instalados (`pip install pygame`).
2. **Execução:** Execute o arquivo principal com `python main.py`.
3. **Início:** Insira os nomes dos jogadores (até 12 caracteres).
4. **Aposta:** - Digite o valor no campo "BET AMOUNT" (até 3 dígitos).
   - Clique na área desejada do tabuleiro ou nos botões laterais.
5. **Resultado:** O resultado do dado é processado e o turno passa para o próximo jogador.
6. **Fim:** Após 5 rodadas ou falência, o vencedor é anunciado. Pressione `R` para reiniciar ou `S` para sair.

## 👨‍💻 Autor
**Francisco Irlan de Oliveira Barros** Estudante de Ciência da Computação - Universidade Federal do Cariri (UFCA)

---
*Projeto desenvolvido para a disciplina de Laboratório de Programação*