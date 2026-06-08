import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ChartBuilder:
    """Build Plotly visualizations for backtest results."""

    def price_with_signals(self, df: pd.DataFrame, symbol: str) -> go.Figure:
        """Create a price chart with SMA lines and buy/sell markers."""
        figure = go.Figure(layout=go.Layout(template="plotly_dark"))

        figure.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close", line=dict(color="lightgray")))
        if "SMA_Short" in df.columns:
            figure.add_trace(go.Scatter(x=df["Date"], y=df["SMA_Short"], mode="lines", name="SMA_Short", line=dict(color="blue", dash="dash")))
        if "SMA_Long" in df.columns:
            figure.add_trace(go.Scatter(x=df["Date"], y=df["SMA_Long"], mode="lines", name="SMA_Long", line=dict(color="orange", dash="dash")))

        buy_signals = df[df["Position"] == 1.0]
        sell_signals = df[df["Position"] == -1.0]

        figure.add_trace(
            go.Scatter(
                x=buy_signals["Date"],
                y=buy_signals["Close"],
                mode="markers",
                name="Buy",
                marker=dict(symbol="triangle-up", color="green", size=10),
            )
        )
        figure.add_trace(
            go.Scatter(
                x=sell_signals["Date"],
                y=sell_signals["Close"],
                mode="markers",
                name="Sell",
                marker=dict(symbol="triangle-down", color="red", size=10),
            )
        )

        figure.update_layout(
            title=f"{symbol} — Golden Cross Strategy",
            xaxis_title="Date",
            yaxis_title="Price",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            template="plotly_dark",
        )
        return figure

    def equity_curve(self, df: pd.DataFrame, initial_capital: float, symbol: str) -> go.Figure:
        """Create an equity curve chart and buy-and-hold comparison."""
        figure = go.Figure(layout=go.Layout(template="plotly_dark"))

        if not df.empty and "Portfolio_Value" in df.columns:
            figure.add_trace(go.Scatter(x=df["Date"], y=df["Portfolio_Value"], mode="lines", name="Portfolio Value", line=dict(color="blue", width=2)))

        if not df.empty and "Close" in df.columns:
            shares_bh = initial_capital / float(df["Close"].iloc[0])
            buy_hold_value = shares_bh * df["Close"]
            figure.add_trace(go.Scatter(x=df["Date"], y=buy_hold_value, mode="lines", name="Buy & Hold", line=dict(color="gray", dash="dot")))

        final_portfolio_value = float(df["Portfolio_Value"].iloc[-1]) if not df.empty and "Portfolio_Value" in df.columns else 0.0
        final_buy_hold_value = float(buy_hold_value.iloc[-1]) if not df.empty and "Close" in df.columns else 0.0

        figure.update_layout(
            title="Portfolio Value vs Buy & Hold",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark",
        )
        figure.add_annotation(
            x=df["Date"].iloc[-1],
            y=final_portfolio_value,
            xref="x",
            yref="y",
            text=f"Portfolio: {final_portfolio_value:.2f}<br>Buy & Hold: {final_buy_hold_value:.2f}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
        )
        return figure

    def drawdown_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create a drawdown percentage chart."""
        figure = go.Figure(layout=go.Layout(template="plotly_dark"))

        if "Portfolio_Value" in df.columns:
            rolling_max = df["Portfolio_Value"].cummax()
            drawdown_pct = (df["Portfolio_Value"] - rolling_max) / rolling_max * 100
            figure.add_trace(go.Scatter(x=df["Date"], y=drawdown_pct, mode="lines", fill="tozeroy", name="Drawdown", line=dict(color="red"), fillcolor="rgba(255, 0, 0, 0.4)"))

        figure.add_hline(y=0, line=dict(color="black", width=1, dash="solid"))
        figure.update_layout(
            title="Drawdown (%)",
            xaxis_title="Date",
            yaxis_title="Percent",
            template="plotly_dark",
        )
        return figure

    def combined_dashboard(self, df: pd.DataFrame, symbol: str, initial_capital: float) -> go.Figure:
        """Create a combined dashboard of signal, equity, and drawdown charts."""
        figure = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.5, 0.3, 0.2], vertical_spacing=0.05)

        price_figure = self.price_with_signals(df, symbol)
        equity_figure = self.equity_curve(df, initial_capital, symbol)
        drawdown_figure = self.drawdown_chart(df)

        for trace in price_figure.data:
            figure.add_trace(trace, row=1, col=1)
        for trace in equity_figure.data:
            figure.add_trace(trace, row=2, col=1)
        for trace in drawdown_figure.data:
            figure.add_trace(trace, row=3, col=1)

        figure.update_layout(title_text=f"{symbol} Backtest Dashboard", template="plotly_dark", showlegend=True)
        return figure
