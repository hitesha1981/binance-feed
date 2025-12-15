import os
import json
import time
import websocket
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

class BinanceFeed:
    def __init__(self):
        self.ws_url = "wss://stream.testnet.binance.vision/stream"
        self.api_key = os.getenv('BINANCE_TESTNET_API_KEY')
        self.symbol = os.getenv('SYMBOL', 'btcusdt').lower()
        
        # Track sequence
        self.seq = 0
        self.last_trade_id = None
        
        # Start connection
        self.connect()
    
    def connect(self):
        """Connect to WebSocket"""
        streams = f"{self.symbol}@trade/{self.symbol}@bookTicker"
        url = f"{self.ws_url}?streams={streams}"
        
        self.ws = websocket.WebSocketApp(
            url,
            on_open=lambda ws: print(f"✅ Connected to {self.symbol.upper()}"),
            on_message=self.on_message,
            on_error=lambda ws, e: print(f"⚠️ Error: {e}"),
            on_close=lambda ws, c, m: self.reconnect(),
            header={"X-MBX-APIKEY": self.api_key} if self.api_key else {}
        )
        
        # Run in background thread
        import threading
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()
    
    def reconnect(self):
        """Auto-reconnect after delay"""
        print("🔄 Reconnecting in 3s...")
        time.sleep(3)
        self.connect()
    
    def on_message(self, ws, message):
        """Process and display all messages"""
        try:
            data = json.loads(message)
            if 'stream' not in data:
                return
            
            self.seq += 1
            stream_data = data['data']
            stream_name = data['stream'].split('@')[1]
            
            # Get server time and calculate latency
            server_time = stream_data.get('E') or stream_data.get('T')
            local_time = time.time_ns() / 1_000_000
            
            if server_time:
                latency = local_time - server_time
                latency_str = f"⏱️ {latency:+.1f}ms"
            else:
                latency_str = ""
            
            # Check for missing trades
            trade_gap = ""
            if 'trade' in stream_name and 't' in stream_data:
                current_id = int(stream_data['t'])
                if self.last_trade_id and current_id > self.last_trade_id + 1:
                    gap = current_id - self.last_trade_id - 1
                    trade_gap = f"⚠️ GAP:{gap}"
                self.last_trade_id = current_id
            
            # Format output
            output = f"[{self.seq:04d}] {stream_name:12} {latency_str}"
            
            # Add message-specific data
            if stream_name == 'trade':
                side = "BUY" if not stream_data.get('m', False) else "SELL"
                output += f" | ${stream_data['p']}×{stream_data['q']} {side}"
                if 't' in stream_data:
                    output += f" ID:{stream_data['t']}"
            elif stream_name == 'bookTicker':
                output += f" | BID:${stream_data['b']} ASK:${stream_data['a']}"
            
            print(output + trade_gap)
            
        except Exception as e:
            print(f"❌ Parse error: {e}")
    
    def run(self):
        """Keep main thread alive"""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n📊 Final: {self.seq} messages")
            if self.ws:
                self.ws.close()

# Run it
if __name__ == "__main__":
    load_dotenv()
    feed = BinanceFeed()
    feed.run()