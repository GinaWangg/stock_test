import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface CurrentPrice {
  price: number | null;
  pct: number | null;
  time: string | null;
}

export interface WatchlistItem {
  stock_id: string;
  name_zh: string;
  is_new: boolean;
  order_index: number;
  last_month_revenue: number | null;
  last_month_yoy: number | null;
  prev_month_revenue: number | null;
  prev_month_yoy: number | null;
  last_quarter_revenue: number | null;
  last_quarter_yoy: number | null;
  current_price: CurrentPrice | null;
}

export const watchlistApi = {
  getWatchlist: async (sort: string = 'prev_month_desc'): Promise<WatchlistItem[]> => {
    const response = await api.get(`/api/watchlist?sort=${sort}`);
    return response.data;
  },

  addToWatchlist: async (stockId: string): Promise<WatchlistItem> => {
    const response = await api.post('/api/watchlist', { stock_id: stockId });
    return response.data;
  },

  removeFromWatchlist: async (stockId: string): Promise<void> => {
    await api.delete(`/api/watchlist/${stockId}`);
  },

  updateWatchlistItem: async (
    stockId: string,
    data: { is_new?: boolean; order_index?: number }
  ): Promise<WatchlistItem> => {
    const response = await api.patch(`/api/watchlist/${stockId}`, data);
    return response.data;
  },
};

export const stocksApi = {
  getStockDetail: async (stockId: string) => {
    const response = await api.get(`/api/stocks/${stockId}`);
    return response.data;
  },

  getMonthlyRevenue: async (stockId: string, start?: string, end?: string) => {
    const params = new URLSearchParams();
    if (start) params.append('start', start);
    if (end) params.append('end', end);
    const response = await api.get(`/api/stocks/${stockId}/monthly_revenue?${params}`);
    return response.data;
  },
};

export const pricesApi = {
  getPrices: async (stockIds: string[]) => {
    const response = await api.get(`/api/prices?stocks=${stockIds.join(',')}`);
    return response.data;
  },
};
