'use client';

import { useState, useEffect } from 'react';
import useSWR from 'swr';
import { watchlistApi, WatchlistItem } from '@/lib/api';
import WatchlistTable from '@/components/WatchlistTable';
import WatchlistCards from '@/components/WatchlistCards';
import AddStockModal from '@/components/AddStockModal';

const fetcher = () => watchlistApi.getWatchlist();

export default function Home() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  
  const { data: watchlist, error, mutate } = useSWR<WatchlistItem[]>('/api/watchlist', fetcher, {
    refreshInterval: 60000, // Refresh every minute
    revalidateOnFocus: true,
  });

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleAddStock = async (stockId: string) => {
    setIsAdding(true);
    try {
      await watchlistApi.addToWatchlist(stockId);
      mutate(); // Refresh data
      setIsModalOpen(false);
      alert(`成功新增股票 ${stockId}`);
    } catch (error: any) {
      const message = error.response?.data?.detail || '新增失敗';
      alert(`新增失敗: ${message}`);
    } finally {
      setIsAdding(false);
    }
  };

  const handleDeleteStock = async (stockId: string) => {
    if (!confirm(`確定要刪除股票 ${stockId} 嗎？`)) {
      return;
    }

    try {
      await watchlistApi.removeFromWatchlist(stockId);
      mutate(); // Refresh data
      alert(`成功刪除股票 ${stockId}`);
    } catch (error: any) {
      const message = error.response?.data?.detail || '刪除失敗';
      alert(`刪除失敗: ${message}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              股票營收觀察工具
            </h1>
            <div className="flex gap-2">
              <button
                onClick={() => setIsModalOpen(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                新增
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md text-red-800">
            載入資料時發生錯誤
          </div>
        )}

        {!watchlist ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">載入中...</p>
          </div>
        ) : (
          <>
            {isMobile ? (
              <WatchlistCards items={watchlist} onDelete={handleDeleteStock} />
            ) : (
              <WatchlistTable items={watchlist} onDelete={handleDeleteStock} />
            )}
          </>
        )}
      </main>

      {/* Add Stock Modal */}
      <AddStockModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAdd={handleAddStock}
        isLoading={isAdding}
      />
    </div>
  );
}
