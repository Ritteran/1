"""
Stock Analyzer Module
Calculates various metrics and technical indicators for stocks
"""

from typing import Dict, Any, Optional
import math


class StockAnalyzer:
    """Analyze stock data and calculate metrics"""

    def __init__(self):
        pass

    def analyze_quote(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a stock quote

        Args:
            quote: Stock quote dictionary from NSE scraper

        Returns:
            Dictionary with analysis results
        """
        if not quote:
            return {}

        analysis = {
            'basic_info': self._analyze_basic_info(quote),
            'price_analysis': self._analyze_price(quote),
            'volume_analysis': self._analyze_volume(quote),
            'valuation': self._analyze_valuation(quote),
            'technical_indicators': self._calculate_technical_indicators(quote),
            'signals': self._generate_signals(quote),
            'risk_metrics': self._analyze_risk(quote)
        }

        return analysis

    def _analyze_basic_info(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and format basic company information"""
        return {
            'symbol': quote.get('symbol', ''),
            'company_name': quote.get('company_name', ''),
            'industry': quote.get('industry', ''),
            'isin': quote.get('isin', ''),
            'last_updated': quote.get('scraped_at', '')
        }

    def _analyze_price(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze price movements and trends"""
        last_price = quote.get('last_price', 0)
        open_price = quote.get('open', 0)
        prev_close = quote.get('previous_close', 0)
        day_high = quote.get('day_high', 0)
        day_low = quote.get('day_low', 0)
        week_52_high = quote.get('week_52_high', 0)
        week_52_low = quote.get('week_52_low', 0)
        change = quote.get('change', 0)
        pchange = quote.get('pChange', 0)

        # Calculate day range percentage
        day_range = ((last_price - day_low) / (day_high - day_low) * 100) if (day_high - day_low) > 0 else 50

        # Calculate 52-week range percentage
        week_52_range = ((last_price - week_52_low) / (week_52_high - week_52_low) * 100) if (week_52_high - week_52_low) > 0 else 50

        # Distance from 52-week high
        distance_from_high = ((week_52_high - last_price) / week_52_high * 100) if week_52_high > 0 else 0

        # Distance from 52-week low
        distance_from_low = ((last_price - week_52_low) / week_52_low * 100) if week_52_low > 0 else 0

        return {
            'last_price': last_price,
            'change': change,
            'pChange': pchange,
            'day_range_pct': day_range,
            'week_52_range_pct': week_52_range,
            'distance_from_52w_high': distance_from_high,
            'distance_from_52w_low': distance_from_low,
            'intraday_gain': ((last_price - open_price) / open_price * 100) if open_price > 0 else 0,
            'volatility_score': self._calculate_volatility_score(day_high, day_low, prev_close)
        }

    def _analyze_volume(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trading volume"""
        volume = quote.get('total_traded_volume', 0)
        value = quote.get('total_traded_value', 0)
        delivery_pct = quote.get('delivery_percentage', 0)
        delivery_qty = quote.get('delivery_quantity', 0)

        # Average price per share traded
        avg_price = (value / volume) if volume > 0 else 0

        # Delivery strength
        delivery_strength = 'Strong' if delivery_pct > 60 else 'Moderate' if delivery_pct > 40 else 'Weak'

        return {
            'volume': volume,
            'value': value,
            'avg_traded_price': avg_price,
            'delivery_percentage': delivery_pct,
            'delivery_quantity': delivery_qty,
            'delivery_strength': delivery_strength
        }

    def _analyze_valuation(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze valuation metrics"""
        pe_ratio = quote.get('pe_ratio', 0)
        market_cap = quote.get('market_cap', 0)
        book_value = quote.get('book_value', 0)
        face_value = quote.get('face_value', 0)
        dividend_yield = quote.get('dividend_yield', 0)
        last_price = quote.get('last_price', 0)

        # Price to Book ratio
        pb_ratio = (last_price / book_value) if book_value > 0 else 0

        # Market cap category
        if market_cap > 100000:  # > 1 Lakh Crore
            cap_category = 'Large Cap'
        elif market_cap > 25000:  # 25K - 1L Crore
            cap_category = 'Mid Cap'
        else:
            cap_category = 'Small Cap'

        # Valuation assessment
        valuation = 'Unknown'
        if pe_ratio > 0:
            if pe_ratio < 15:
                valuation = 'Undervalued'
            elif pe_ratio < 25:
                valuation = 'Fairly Valued'
            elif pe_ratio < 40:
                valuation = 'Overvalued'
            else:
                valuation = 'Highly Overvalued'

        return {
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'market_cap': market_cap,
            'market_cap_category': cap_category,
            'book_value': book_value,
            'face_value': face_value,
            'dividend_yield': dividend_yield,
            'valuation_assessment': valuation
        }

    def _calculate_technical_indicators(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate technical indicators"""
        last_price = quote.get('last_price', 0)
        day_high = quote.get('day_high', 0)
        day_low = quote.get('day_low', 0)
        prev_close = quote.get('previous_close', 0)
        open_price = quote.get('open', 0)

        # RSI-like indicator (simplified using daily data)
        price_momentum = ((last_price - prev_close) / prev_close * 100) if prev_close > 0 else 0

        # Support and Resistance levels
        support_level = day_low
        resistance_level = day_high

        # Pivot point
        pivot = (day_high + day_low + last_price) / 3

        return {
            'price_momentum': price_momentum,
            'support_level': support_level,
            'resistance_level': resistance_level,
            'pivot_point': pivot,
            'distance_from_support': ((last_price - support_level) / support_level * 100) if support_level > 0 else 0,
            'distance_from_resistance': ((resistance_level - last_price) / last_price * 100) if last_price > 0 else 0
        }

    def _generate_signals(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signals based on analysis"""
        pchange = quote.get('pChange', 0)
        last_price = quote.get('last_price', 0)
        week_52_high = quote.get('week_52_high', 0)
        week_52_low = quote.get('week_52_low', 0)
        delivery_pct = quote.get('delivery_percentage', 0)
        pe_ratio = quote.get('pe_ratio', 0)

        # Calculate 52-week position
        week_52_range = week_52_high - week_52_low
        position_in_range = ((last_price - week_52_low) / week_52_range * 100) if week_52_range > 0 else 50

        # Signals
        signals = []
        overall_signal = 'NEUTRAL'
        confidence = 0

        # Price momentum signal
        if pchange > 3:
            signals.append('📈 Strong Upward Momentum')
            confidence += 20
        elif pchange > 1:
            signals.append('↗️ Positive Momentum')
            confidence += 10
        elif pchange < -3:
            signals.append('📉 Strong Downward Momentum')
            confidence -= 20
        elif pchange < -1:
            signals.append('↘️ Negative Momentum')
            confidence -= 10

        # 52-week position signal
        if position_in_range > 80:
            signals.append('🔥 Near 52-Week High')
            confidence += 15
        elif position_in_range < 20:
            signals.append('💎 Near 52-Week Low')
            confidence += 15

        # Delivery signal
        if delivery_pct > 60:
            signals.append('💪 Strong Delivery Percentage')
            confidence += 15
        elif delivery_pct < 30:
            signals.append('⚠️ Weak Delivery Percentage')
            confidence -= 10

        # Valuation signal
        if 0 < pe_ratio < 15:
            signals.append('💰 Attractive Valuation (Low P/E)')
            confidence += 10
        elif pe_ratio > 40:
            signals.append('⚠️ High Valuation (High P/E)')
            confidence -= 10

        # Overall signal
        if confidence > 30:
            overall_signal = 'BUY'
        elif confidence > 10:
            overall_signal = 'ACCUMULATE'
        elif confidence < -30:
            overall_signal = 'SELL'
        elif confidence < -10:
            overall_signal = 'REDUCE'
        else:
            overall_signal = 'HOLD'

        return {
            'overall_signal': overall_signal,
            'confidence_score': confidence,
            'signals': signals,
            'position_in_52w_range': position_in_range
        }

    def _analyze_risk(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk factors"""
        upper_circuit = quote.get('upper_circuit', 0)
        lower_circuit = quote.get('lower_circuit', 0)
        last_price = quote.get('last_price', 0)
        day_high = quote.get('day_high', 0)
        day_low = quote.get('day_low', 0)

        # Distance from circuits
        distance_upper = ((upper_circuit - last_price) / last_price * 100) if last_price > 0 else 0
        distance_lower = ((last_price - lower_circuit) / last_price * 100) if last_price > 0 else 0

        # Intraday volatility
        intraday_vol = ((day_high - day_low) / day_low * 100) if day_low > 0 else 0

        # Risk level
        if intraday_vol < 2:
            risk_level = 'Low'
        elif intraday_vol < 5:
            risk_level = 'Moderate'
        elif intraday_vol < 8:
            risk_level = 'High'
        else:
            risk_level = 'Very High'

        # Circuit warnings
        circuit_warnings = []
        if distance_upper < 2:
            circuit_warnings.append('⚠️ Close to Upper Circuit')
        if distance_lower < 2:
            circuit_warnings.append('⚠️ Close to Lower Circuit')

        return {
            'risk_level': risk_level,
            'intraday_volatility': intraday_vol,
            'distance_from_upper_circuit': distance_upper,
            'distance_from_lower_circuit': distance_lower,
            'circuit_warnings': circuit_warnings
        }

    def _calculate_volatility_score(self, high: float, low: float, prev_close: float) -> float:
        """Calculate volatility score (0-100)"""
        if prev_close == 0:
            return 0

        day_range = high - low
        volatility = (day_range / prev_close) * 100

        # Normalize to 0-100 scale (assume 10% is max volatility)
        score = min(volatility * 10, 100)

        return round(score, 2)
