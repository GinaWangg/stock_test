import React, { useState } from 'react';

interface AddStockModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAdd: (stockId: string) => void;
  isLoading: boolean;
}

export default function AddStockModal({ isOpen, onClose, onAdd, isLoading }: AddStockModalProps) {
  const [stockId, setStockId] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (stockId.trim()) {
      onAdd(stockId.trim());
      setStockId('');
    }
  };

  const handleClose = () => {
    setStockId('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
        <div className="p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">新增股票到追蹤清單</h2>
          
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="stockId" className="block text-sm font-medium text-gray-700 mb-2">
                股票代碼
              </label>
              <input
                type="text"
                id="stockId"
                value={stockId}
                onChange={(e) => setStockId(e.target.value)}
                placeholder="例如：2330"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
                autoFocus
              />
              <p className="mt-1 text-sm text-gray-500">
                請輸入台股代碼（例如：2330、2317、2454）
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <button
                type="button"
                onClick={handleClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                disabled={isLoading}
              >
                取消
              </button>
              <button
                type="submit"
                disabled={!stockId.trim() || isLoading}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {isLoading ? '處理中...' : '新增'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
