# 🧠 Liquidity Hunter

**Liquidity Hunter** é um sistema backend automatizado para envio de sinais de trade no Telegram, baseado na metodologia ICT/SMC (*Smart Money Concepts*).

O sistema identifica zonas de liquidez institucional com alta precisão, valida os sinais por meio de Inteligência Artificial e envia alertas com imagem e texto para o Telegram com antecedência ideal.  
Seu foco está em detectar sinais com alto índice de acerto, respeitando critérios rigorosos como RR mínimo de 2:1, confluência de fatores técnicos e probabilidade real de alcançar o Take Profit.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10 (via Docker)
- PostgreSQL (com persistência)
- APScheduler (agendador automático)
- scikit-learn + XGBoost (IA supervisionada)
- Matplotlib (visualização dos sinais)
- Telegram Bot API (envio de alertas)
- Estrutura de logs em `.jsonl` por rodada

---

## 🧠 Funcionalidades

- Detectores ICT: OTE, OB, FVG, Sweep, CHoCH/MSS
- Sinais enviados apenas se:
  - RR ≥ 2
  - 3 ou mais confluências
  - Score IA positivo
- Verificação automática de TP/SL
- Aprendizado contínuo com base em resultados reais
- Visualização automática do sinal com imagem
- Envio de alertas diretamente no Telegram
- Log estruturado por rodada com performance

---

## 👨‍💻 Desenvolvedor

**Peter Freitas**  
📧 opeterfreitas@gmail.com  
🔗 [github.com/opeterfreitas](https://github.com/opeterfreitas)

---

## 🛡️ Licença

Projeto privado. O uso ou distribuição sem permissão expressa do autor é proibido.
