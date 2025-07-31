import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Lista de ações para análise (ações de maior relevância e volume)
acoes = [
    'BOVA11.SA', 'VALE3.SA', 'PETR4.SA', 'BBAS3.SA', 'ITUB3.SA', 'MGLU3.SA',
    'ABEV3.SA', 'B3SA3.SA', 'BRFS3.SA', 'GGBR4.SA', 'LREN3.SA', 'RENT3.SA',
    'SUZB3.SA', 'WEGE3.SA', 'JBSS3.SA', 'CSNA3.SA', 'ELET3.SA', 'PRIO3.SA',
    'RAIL3.SA', 'BRKM5.SA', 'HAPV3.SA', 'CYRE3.SA', 'EGIE3.SA', 'CPLE6.SA',
    'TAEE11.SA', 'VIVT3.SA', 'TIMS3.SA', 'COGN3.SA', 'AZUL4.SA', 'GOLL4.SA'
]

# Função para carregar dados de cada ação separadamente
@st.cache_data(ttl=3600)
def carregar_dados(acao):
    dados = yf.download(acao, period='1y', interval='1d')
    return dados






st.set_page_config(page_title="Análise de Ações", page_icon="📈", layout="wide")
st.markdown("""
<style>
.main-title {font-size: 2.5em; font-weight: bold; color: #1a237e; margin-bottom: 0.2em;}
.subtitle {font-size: 1.2em; color: #3949ab; margin-bottom: 1em;}
.section-title {font-size: 1.1em; color: #1565c0; margin-top: 1.5em; margin-bottom: 0.5em;}
.stPlotlyChart {background: #f5f5f5; border-radius: 10px; padding: 10px;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-title">📈 Análise de Mercado de Ações</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dashboard interativo com os principais indicadores e gráficos para análise profissional das ações brasileiras.</div>', unsafe_allow_html=True)
st.markdown("""
<hr style='border:1px solid #3949ab; margin-top:0.5em; margin-bottom:1em;'>
""", unsafe_allow_html=True)

# Explicações dos gráficos
explicacoes = {
    'Preço de Fechamento': "Mostra o valor de fechamento diário da ação. Ajuda a visualizar a tendência geral do preço ao longo do tempo.",
    'Candlestick': "Representa a variação de preço (abertura, máxima, mínima, fechamento) de cada dia. Facilita a identificação de padrões de reversão e continuidade.",
    'Volume Negociado': "Exibe o volume de ações negociadas por dia. Volumes altos podem indicar interesse institucional ou eventos relevantes.",
    'Média Móvel': "Suaviza as oscilações do preço, mostrando a tendência média em determinado período. Cruzamentos podem indicar pontos de compra/venda.",
    'Retorno Diário': "Mostra a variação percentual diária do preço. Útil para identificar dias de maior volatilidade.",
    'Volatilidade': "Indica o grau de variação dos retornos. Volatilidade alta sugere maior risco e potencial de movimentos bruscos.",
    'Candlestick Intradiário': "Mostra a variação de preço ao longo do último dia útil, com dados por hora. Útil para análise de movimentos intradiários.",
    'RSI': "Índice de Força Relativa. Mede o ritmo das variações de preço, indicando sobrecompra (>70) ou sobrevenda (<30).",
    'MACD': "Compara médias móveis para identificar mudanças de tendência. Cruzamentos entre MACD e sua linha de sinal sugerem compra/venda.",
    'Estocástico': "Compara o preço de fechamento com a faixa de preços recente. Valores altos indicam sobrecompra, baixos indicam sobrevenda.",
    'Bandas de Bollinger': "Mostra faixas de preço baseadas na volatilidade. Preços próximos às bandas podem indicar reversão ou continuação da tendência.",
    'Williams %R': "Oscilador que indica condições de sobrecompra/sobrevenda. Valores próximos de -100 sugerem sobrevenda, próximos de 0 sugerem sobrecompra.",
    'ADX': "Mede a força da tendência, independentemente da direção. Valores acima de 25 indicam tendência forte.",
    'OBV': "On Balance Volume. Relaciona volume e preço para identificar acumulação/distribuição. Divergências podem antecipar movimentos.",
    'MFI': "Money Flow Index. Combina preço e volume para indicar sobrecompra/sobrevenda. Valores acima de 80 ou abaixo de 20 são extremos.",
    'EMA 50/200': "Médias móveis exponenciais de 50 e 200 dias. Cruzamentos entre elas são usados para identificar tendências de longo prazo.",
    'ROC': "Rate of Change. Mede a variação percentual do preço em relação a períodos anteriores. Útil para identificar aceleração ou desaceleração da tendência."
}



# Caixa de seleção no topo da barra lateral
acao_selecionada = st.sidebar.selectbox("Selecione a ação para análise:", acoes)

# Carregar dados
dados = carregar_dados(acao_selecionada)

# Estatísticas resumidas na barra lateral
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<b>📊 Estatísticas Resumidas</b>", unsafe_allow_html=True)
if not dados.empty:
    if isinstance(dados.columns, pd.MultiIndex):
        dados_acao = pd.DataFrame({
            'Date': dados.index,
            'Open': dados['Open', acao_selecionada],
            'High': dados['High', acao_selecionada],
            'Low': dados['Low', acao_selecionada],
            'Close': dados['Close', acao_selecionada],
            'Volume': dados['Volume', acao_selecionada]
        })
    else:
        dados_acao = dados.reset_index()

    preco_atual = dados_acao['Close'].iloc[-1]
    st.sidebar.write(f"Preço atual: **R$ {preco_atual:.2f}**")
    if len(dados_acao) > 22:
        variacao_1m = ((preco_atual/dados_acao['Close'].iloc[-22]-1)*100)
        st.sidebar.write(f"Variação 1 mês: **{variacao_1m:.2f}%**")
    if len(dados_acao) > 1:
        variacao_1a = ((preco_atual/dados_acao['Close'].iloc[0]-1)*100)
        st.sidebar.write(f"Variação 1 ano: **{variacao_1a:.2f}%**")
    if len(dados_acao) > 132:
        variacao_6m = ((preco_atual/dados_acao['Close'].iloc[-132]-1)*100)
        st.sidebar.write(f"Variação 6 meses: **{variacao_6m:.2f}%**")

    # Indicadores fundamentalistas (mock)
    # Em produção, buscar dados reais de fontes como Fundamentus, StatusInvest, etc.
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("<b>📈 Indicadores Fundamentalistas</b>", unsafe_allow_html=True)
    # Mock para exemplo
    pl = 10.5
    pvp = 1.8
    div_liq_patr = 0.7
    div_liq_ebitda = 2.1
    div_liq_ebit = 2.5
    div_bruta_patr = 1.2
    liquidez_corrente = 1.6
    st.sidebar.write(f"P/L: **{pl:.2f}**")
    st.sidebar.write(f"P/VP: **{pvp:.2f}**")
    st.sidebar.write(f"Dívida Líquida/Patrimônio: **{div_liq_patr:.2f}**")
    st.sidebar.write(f"Dívida Líquida/EBITDA: **{div_liq_ebitda:.2f}**")
    st.sidebar.write(f"Dívida Líquida/EBIT: **{div_liq_ebit:.2f}**")
    st.sidebar.write(f"Dívida Bruta/Patrimônio: **{div_bruta_patr:.2f}**")
    st.sidebar.write(f"Liquidez Corrente: **{liquidez_corrente:.2f}**")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

if dados.empty:
    st.warning(f"Não foi possível obter dados para {acao_selecionada}.")
else:
    st.subheader(f"Dados históricos de {acao_selecionada}")
    # Se vier multi-index, pega só a coluna da ação selecionada
    if isinstance(dados.columns, pd.MultiIndex):
        dados_acao = pd.DataFrame({
            'Date': dados.index,
            'Open': dados['Open', acao_selecionada],
            'High': dados['High', acao_selecionada],
            'Low': dados['Low', acao_selecionada],
            'Close': dados['Close', acao_selecionada],
            'Volume': dados['Volume', acao_selecionada]
        })
    else:
        dados_acao = dados.reset_index()


    st.markdown('<div class="section-title">Tabela de Dados Recentes</div>', unsafe_allow_html=True)
    st.dataframe(dados_acao[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].tail(30), use_container_width=True)
    st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)



    st.markdown('<div class="section-title">Gráfico de Preço de Fechamento</div>', unsafe_allow_html=True)
    fig_close = px.line(dados_acao, x='Date', y='Close', title=f'Preço de Fechamento - {acao_selecionada}', color_discrete_sequence=['#3949ab'])
    st.plotly_chart(fig_close, use_container_width=True)
    st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


    st.markdown('<div class="section-title">Gráfico Candlestick</div>', unsafe_allow_html=True)
    fig_candle = go.Figure(data=[go.Candlestick(
        x=dados_acao['Date'],
        open=dados_acao['Open'],
        high=dados_acao['High'],
        low=dados_acao['Low'],
        close=dados_acao['Close']
    )])
    fig_candle.update_layout(title=f'Candlestick - {acao_selecionada}', xaxis_title='Data', yaxis_title='Preço', plot_bgcolor='#f5f5f5')
    st.plotly_chart(fig_candle, use_container_width=True)
    st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


    st.markdown('<div class="section-title">Gráfico de Volume Negociado</div>', unsafe_allow_html=True)
    fig_vol = px.bar(dados_acao, x='Date', y='Volume', title=f'Volume Negociado - {acao_selecionada}', color_discrete_sequence=['#1565c0'])
    st.plotly_chart(fig_vol, use_container_width=True)
    st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)

# Gráfico de Média Móvel de 21 dias
st.markdown('<div class="section-title">Média Móvel de 21 dias</div>', unsafe_allow_html=True)
dados_acao['MM21'] = dados_acao['Close'].rolling(window=21).mean()
fig_mm = px.line(dados_acao, x='Date', y=['Close', 'MM21'], title=f'Média Móvel 21 dias - {acao_selecionada}', color_discrete_sequence=['#3949ab', '#e53935'])
st.plotly_chart(fig_mm, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


# Gráfico de Retorno Percentual Diário
st.markdown('<div class="section-title">Retorno Percentual Diário</div>', unsafe_allow_html=True)
dados_acao['Retorno'] = dados_acao['Close'].pct_change()*100
fig_ret = px.bar(dados_acao, x='Date', y='Retorno', title=f'Retorno Diário (%) - {acao_selecionada}', color_discrete_sequence=['#e53935'])
st.plotly_chart(fig_ret, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


# Gráfico de Volatilidade (Desvio Padrão dos retornos, janela de 21 dias)
st.markdown('<div class="section-title">Volatilidade (21 dias)</div>', unsafe_allow_html=True)
dados_acao['Volatilidade'] = dados_acao['Retorno'].rolling(window=21).std()
fig_volat = px.line(dados_acao, x='Date', y='Volatilidade', title=f'Volatilidade 21 dias (%) - {acao_selecionada}', color_discrete_sequence=['#43a047'])
st.plotly_chart(fig_volat, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


# Indicadores adicionais
st.markdown('<div class="section-title">Indicadores Técnicos</div>', unsafe_allow_html=True)
dados_acao['MM9'] = dados_acao['Close'].rolling(window=9).mean()
dados_acao['MM50'] = dados_acao['Close'].rolling(window=50).mean()
fig_mm_multi = px.line(dados_acao, x='Date', y=['Close', 'MM9', 'MM21', 'MM50'], title=f'Médias Móveis - {acao_selecionada}', color_discrete_sequence=['#3949ab', '#e53935', '#43a047', '#fbc02d'])
st.plotly_chart(fig_mm_multi, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


# RSI (Relative Strength Index)
def calcula_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
dados_acao['RSI'] = calcula_rsi(dados_acao)
fig_rsi = px.line(dados_acao, x='Date', y='RSI', title=f'RSI (14 períodos) - {acao_selecionada}', color_discrete_sequence=['#e53935'])
st.plotly_chart(fig_rsi, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


# MACD (Moving Average Convergence Divergence)
st.markdown('<div class="section-title">MACD</div>', unsafe_allow_html=True)
exp12 = dados_acao['Close'].ewm(span=12, adjust=False).mean()
exp26 = dados_acao['Close'].ewm(span=26, adjust=False).mean()
dados_acao['MACD'] = exp12 - exp26
dados_acao['MACD_signal'] = dados_acao['MACD'].ewm(span=9, adjust=False).mean()
fig_macd = px.line(dados_acao, x='Date', y=['MACD', 'MACD_signal'], title=f'MACD - {acao_selecionada}', color_discrete_sequence=['#3949ab', '#e53935'])
st.plotly_chart(fig_macd, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)


# Estocástico
st.markdown('<div class="section-title">Estocástico</div>', unsafe_allow_html=True)
low_min = dados_acao['Low'].rolling(window=14).min()
high_max = dados_acao['High'].rolling(window=14).max()
dados_acao['%K'] = 100 * ((dados_acao['Close'] - low_min) / (high_max - low_min))
dados_acao['%D'] = dados_acao['%K'].rolling(window=3).mean()
fig_stoc = px.line(dados_acao, x='Date', y=['%K', '%D'], title=f'Estocástico - {acao_selecionada}', color_discrete_sequence=['#43a047', '#e53935'])
st.plotly_chart(fig_stoc, use_container_width=True)
st.markdown("<hr style='border:0.5px solid #e0e0e0; margin-top:1em; margin-bottom:1em;'>", unsafe_allow_html=True)

# Gráfico de Fibonacci (Retração) - Últimos 6 meses
st.markdown('<div class="section-title">Fibonacci (Retração) - Últimos 6 Meses</div>', unsafe_allow_html=True)
dados_fibo_6m = dados_acao.tail(132)
preco_max_6m = dados_fibo_6m['High'].max()
preco_min_6m = dados_fibo_6m['Low'].min()
fibo_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
fibo_values_6m = [preco_max_6m - (preco_max_6m-preco_min_6m)*level for level in fibo_levels]
fig_fibo_6m = go.Figure()
fig_fibo_6m.add_trace(go.Candlestick(
    x=dados_fibo_6m['Date'],
    open=dados_fibo_6m['Open'],
    high=dados_fibo_6m['High'],
    low=dados_fibo_6m['Low'],
    close=dados_fibo_6m['Close'],
    name='Candlestick'))
for i, level in enumerate(fibo_levels):
    fig_fibo_6m.add_shape(type='line', x0=dados_fibo_6m['Date'].iloc[0], x1=dados_fibo_6m['Date'].iloc[-1], y0=fibo_values_6m[i], y1=fibo_values_6m[i],
                      line=dict(color='#fbc02d', width=2, dash='dot'))
    fig_fibo_6m.add_annotation(x=dados_fibo_6m['Date'].iloc[-1], y=fibo_values_6m[i],
        text=f'{int(level*100)}%', showarrow=False, yshift=0, font=dict(color='#fbc02d'))
fig_fibo_6m.update_layout(title=f'Retração de Fibonacci - Últimos 6 Meses ({acao_selecionada})', xaxis_title='Data', yaxis_title='Preço', plot_bgcolor='#f5f5f5')
st.plotly_chart(fig_fibo_6m, use_container_width=True)
st.markdown("<hr style='border:1px solid #3949ab; margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)

# Gráfico de Fibonacci (Retração) - Últimos 3 meses
st.markdown('<div class="section-title">Fibonacci (Retração) - Últimos 3 Meses</div>', unsafe_allow_html=True)
dados_fibo_3m = dados_acao.tail(66)
preco_max_3m = dados_fibo_3m['High'].max()
preco_min_3m = dados_fibo_3m['Low'].min()
fibo_values_3m = [preco_max_3m - (preco_max_3m-preco_min_3m)*level for level in fibo_levels]
fig_fibo_3m = go.Figure()
fig_fibo_3m.add_trace(go.Candlestick(
    x=dados_fibo_3m['Date'],
    open=dados_fibo_3m['Open'],
    high=dados_fibo_3m['High'],
    low=dados_fibo_3m['Low'],
    close=dados_fibo_3m['Close'],
    name='Candlestick'))
for i, level in enumerate(fibo_levels):
    fig_fibo_3m.add_shape(type='line', x0=dados_fibo_3m['Date'].iloc[0], x1=dados_fibo_3m['Date'].iloc[-1], y0=fibo_values_3m[i], y1=fibo_values_3m[i],
                      line=dict(color='#fbc02d', width=2, dash='dot'))
    fig_fibo_3m.add_annotation(x=dados_fibo_3m['Date'].iloc[-1], y=fibo_values_3m[i],
        text=f'{int(level*100)}%', showarrow=False, yshift=0, font=dict(color='#fbc02d'))
fig_fibo_3m.update_layout(title=f'Retração de Fibonacci - Últimos 3 Meses ({acao_selecionada})', xaxis_title='Data', yaxis_title='Preço', plot_bgcolor='#f5f5f5')
st.plotly_chart(fig_fibo_3m, use_container_width=True)
st.markdown("<hr style='border:1px solid #3949ab; margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)

# Bollinger Bands - Últimos 6 meses com Candlestick
st.markdown('### Bollinger Bands - Últimos 6 Meses (Candlestick)')
window = 20
dados_acao['BB_MA'] = dados_acao['Close'].rolling(window=window).mean()
dados_acao['BB_UPPER'] = dados_acao['BB_MA'] + 2*dados_acao['Close'].rolling(window=window).std()
dados_acao['BB_LOWER'] = dados_acao['BB_MA'] - 2*dados_acao['Close'].rolling(window=window).std()
dados_bollinger_6m = dados_acao.tail(132) # Aproximadamente 6 meses de pregão
fig_bb_candle_6m = go.Figure()
fig_bb_candle_6m.add_trace(go.Candlestick(
    x=dados_bollinger_6m['Date'],
    open=dados_bollinger_6m['Open'],
    high=dados_bollinger_6m['High'],
    low=dados_bollinger_6m['Low'],
    close=dados_bollinger_6m['Close'],
    name='Candlestick'))
fig_bb_candle_6m.add_trace(go.Scatter(x=dados_bollinger_6m['Date'], y=dados_bollinger_6m['BB_MA'], mode='lines', name='BB_MA', line=dict(color='blue')))
fig_bb_candle_6m.add_trace(go.Scatter(x=dados_bollinger_6m['Date'], y=dados_bollinger_6m['BB_UPPER'], mode='lines', name='BB_UPPER', line=dict(color='green', dash='dot')))
fig_bb_candle_6m.add_trace(go.Scatter(x=dados_bollinger_6m['Date'], y=dados_bollinger_6m['BB_LOWER'], mode='lines', name='BB_LOWER', line=dict(color='red', dash='dot')))
fig_bb_candle_6m.add_trace(go.Scatter(
    x=pd.concat([dados_bollinger_6m['Date'], dados_bollinger_6m['Date'][::-1]]),
    y=pd.concat([dados_bollinger_6m['BB_UPPER'], dados_bollinger_6m['BB_LOWER'][::-1]]),
    fill='toself', fillcolor='rgba(200,200,255,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Bandas'))
fig_bb_candle_6m.update_layout(title=f'Bollinger Bands - Últimos 6 Meses ({acao_selecionada})', xaxis_title='Data', yaxis_title='Preço')
st.plotly_chart(fig_bb_candle_6m, use_container_width=True)

# Bollinger Bands - 1 ano com Candlestick
st.markdown('### Bollinger Bands - 1 Ano (Candlestick)')
dados_bollinger_ano = dados_acao.tail(252) # Aproximadamente 1 ano de pregão
fig_bb_candle_ano = go.Figure()
fig_bb_candle_ano.add_trace(go.Candlestick(
    x=dados_bollinger_ano['Date'],
    open=dados_bollinger_ano['Open'],
    high=dados_bollinger_ano['High'],
    low=dados_bollinger_ano['Low'],
    close=dados_bollinger_ano['Close'],
    name='Candlestick'))
fig_bb_candle_ano.add_trace(go.Scatter(x=dados_bollinger_ano['Date'], y=dados_bollinger_ano['BB_MA'], mode='lines', name='BB_MA'))
fig_bb_candle_ano.add_trace(go.Scatter(x=dados_bollinger_ano['Date'], y=dados_bollinger_ano['BB_UPPER'], mode='lines', name='BB_UPPER'))
fig_bb_candle_ano.add_trace(go.Scatter(x=dados_bollinger_ano['Date'], y=dados_bollinger_ano['BB_LOWER'], mode='lines', name='BB_LOWER'))
fig_bb_candle_ano.update_layout(title=f'Bollinger Bands - 1 Ano ({acao_selecionada})', xaxis_title='Data', yaxis_title='Preço')
st.plotly_chart(fig_bb_candle_ano, use_container_width=True)


# Indicadores extras
st.markdown('### Indicadores Extras')

# Williams %R
highest_high = dados_acao['High'].rolling(window=14).max()
lowest_low = dados_acao['Low'].rolling(window=14).min()
dados_acao['Williams_%R'] = -100 * ((highest_high - dados_acao['Close']) / (highest_high - lowest_low))
fig_williams = px.line(dados_acao, x='Date', y='Williams_%R', title=f'Williams %R (14 períodos) - {acao_selecionada}')
st.plotly_chart(fig_williams, use_container_width=True)

# Indicadores profissionais adicionais

# 1. ADX (Average Directional Index)
def calcula_adx(df, n=14):
    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff()
    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)
    tr1 = df['High'] - df['Low']
    tr2 = abs(df['High'] - df['Close'].shift())
    tr3 = abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(n).mean()
    plus_di = 100 * (plus_dm.rolling(n).sum() / atr)
    minus_di = 100 * (minus_dm.rolling(n).sum() / atr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(n).mean()
    return adx
dados_acao['ADX'] = calcula_adx(dados_acao)
fig_adx = px.line(dados_acao, x='Date', y='ADX', title=f'ADX (14 períodos) - {acao_selecionada}')
st.plotly_chart(fig_adx, use_container_width=True)

# 2. OBV (On Balance Volume)
dados_acao['OBV'] = (dados_acao['Volume'] * ((dados_acao['Close'] > dados_acao['Close'].shift()).astype(int) - (dados_acao['Close'] < dados_acao['Close'].shift()).astype(int))).cumsum()
fig_obv = px.line(dados_acao, x='Date', y='OBV', title=f'OBV - On Balance Volume - {acao_selecionada}')
st.plotly_chart(fig_obv, use_container_width=True)

# 3. MFI (Money Flow Index)
typical_price = (dados_acao['High'] + dados_acao['Low'] + dados_acao['Close']) / 3
raw_money_flow = typical_price * dados_acao['Volume']
positive_flow = raw_money_flow.where(typical_price > typical_price.shift(), 0)
negative_flow = raw_money_flow.where(typical_price < typical_price.shift(), 0)
positive_mf = positive_flow.rolling(14).sum()
negative_mf = negative_flow.rolling(14).sum()
mfi = 100 * (positive_mf / (positive_mf + negative_mf))
dados_acao['MFI'] = mfi
fig_mfi = px.line(dados_acao, x='Date', y='MFI', title=f'MFI (Money Flow Index) - {acao_selecionada}')
st.plotly_chart(fig_mfi, use_container_width=True)

# 4. EMA 50/200 (Exponential Moving Average)
dados_acao['EMA50'] = dados_acao['Close'].ewm(span=50, adjust=False).mean()
dados_acao['EMA200'] = dados_acao['Close'].ewm(span=200, adjust=False).mean()
fig_ema = px.line(dados_acao, x='Date', y=['Close', 'EMA50', 'EMA200'], title=f'EMA 50/200 - {acao_selecionada}')
st.plotly_chart(fig_ema, use_container_width=True)

# 5. ROC (Rate of Change)
dados_acao['ROC'] = dados_acao['Close'].pct_change(periods=12) * 100
fig_roc = px.line(dados_acao, x='Date', y='ROC', title=f'ROC (Rate of Change 12 períodos) - {acao_selecionada}')
st.plotly_chart(fig_roc, use_container_width=True)