# Stock Revenue Tracking Frontend

Next.js frontend for Taiwan stock revenue observation tool.

## Features

- 📊 Responsive watchlist display (table + cards)
- ➕ Add/delete stocks from watchlist
- 💹 Real-time data updates with SWR
- 📱 Mobile-first design
- 🎨 Tailwind CSS styling
- 🔄 Automatic data refresh (60s)

## Tech Stack

- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- SWR (data fetching)
- Axios (HTTP client)

## Setup

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
# Copy example file
cp .env.local.example .env.local

# Edit .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

3. Run development server:
```bash
npm run dev
```

4. Open browser:
```
http://localhost:3000
```

### GitHub Codespaces

When running in Codespaces, you need to use the forwarded port URL for the backend:

1. Start the backend first (in backend directory):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Get the backend forwarded URL:
   - Click the "PORTS" tab in VS Code (bottom panel)
   - Find port 8000 and copy the forwarded URL
   - It will look like: `https://username-repo-abc123-8000.app.github.dev`

3. Configure frontend environment:
```bash
# Create .env.local with the forwarded URL
echo "NEXT_PUBLIC_API_BASE_URL=https://your-forwarded-url-8000.app.github.dev" > .env.local
```

4. Install and run:
```bash
npm install
npm run dev
```

5. Access the app through port 3000's forwarded URL

**Note**: The forwarded URL changes each time Codespace restarts. Update `.env.local` accordingly.

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page (watchlist)
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── AddStockModal.tsx  # Add stock dialog
│   ├── StockCard.tsx      # Mobile card view
│   ├── StockRow.tsx       # Desktop table row
│   ├── WatchlistCards.tsx # Mobile cards container
│   └── WatchlistTable.tsx # Desktop table
├── lib/                   # Utilities
│   ├── api.ts            # API client functions
│   └── formatters.ts     # Data formatting utilities
├── public/               # Static assets
├── package.json
└── tsconfig.json
```

## Components

### WatchlistTable (Desktop)
Table layout for large screens showing:
- Stock ID and name
- Last month revenue + YoY
- Previous month revenue + YoY
- Last quarter revenue + YoY
- Current price + change %
- Delete action

### WatchlistCards (Mobile)
Card layout for small screens (<768px) with same data in vertical format.

### StockRow
Individual table row component with formatted data.

### StockCard
Individual card component for mobile view.

### AddStockModal
Modal dialog for adding stocks with:
- Stock ID input
- Validation
- Submit/Cancel actions

## Data Formatting

### Revenue Display
```typescript
formatRevenue(revenue: number | null): string
// Input: 251466728000 (元)
// Output: "2,514.67" (億元)
```

### Percentage Display
```typescript
formatPercentage(pct: number | null): string
// Input: 5.18
// Output: "+5.18%"
// Input: -2.34
// Output: "-2.34%"
```

### Color Coding
- Positive YoY: Red (`text-red-600`)
- Negative YoY: Green (`text-green-600`)
- Null/Zero: Gray (`text-gray-500`)

### Empty Values
All null values display as "—"

## API Integration

### Get Watchlist
```typescript
import { watchlistApi } from '@/lib/api';

const watchlist = await watchlistApi.getWatchlist('prev_month_desc');
```

### Add Stock
```typescript
const newItem = await watchlistApi.addToWatchlist('2330');
```

### Delete Stock
```typescript
await watchlistApi.removeFromWatchlist('2330');
```

### Update Stock
```typescript
const updated = await watchlistApi.updateWatchlistItem('2330', {
  is_new: false,
  order_index: 1
});
```

## SWR Configuration

```typescript
useSWR('/api/watchlist', fetcher, {
  refreshInterval: 60000,  // Auto-refresh every 60s
  revalidateOnFocus: true, // Refresh on window focus
});
```

## Responsive Breakpoints

```css
/* Mobile: < 768px */
/* Desktop: >= 768px */
```

Layout automatically switches based on viewport width.

## Styling

Uses Tailwind CSS with custom configuration:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

For production, set to actual backend URL:
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.yourapp.com
```

## TypeScript Types

### WatchlistItem
```typescript
interface WatchlistItem {
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
```

### CurrentPrice
```typescript
interface CurrentPrice {
  price: number | null;
  pct: number | null;
  time: string | null;
}
```

## Error Handling

```typescript
try {
  await watchlistApi.addToWatchlist(stockId);
  alert('成功新增股票');
} catch (error: any) {
  const message = error.response?.data?.detail || '新增失敗';
  alert(`新增失敗: ${message}`);
}
```

## Testing

Run linter:
```bash
npm run lint
```

Type check:
```bash
npm run type-check  # (if configured)
```

## Performance

- **SWR caching**: Reduces API calls
- **Automatic revalidation**: Keeps data fresh
- **Code splitting**: Next.js automatic optimization
- **Image optimization**: Next.js Image component

## Deployment

### Vercel (Recommended)
```bash
vercel
```

### Docker
```bash
docker build -t stock-frontend .
docker run -p 3000:3000 stock-frontend
```

### Static Export
```bash
npm run build
# Deploy 'out' directory to static host
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Screen reader friendly

## Future Enhancements

- [ ] Stock search with autocomplete
- [ ] Price charts integration
- [ ] News modal display
- [ ] Excel export button
- [ ] Dark mode support
- [ ] PWA features
- [ ] Internationalization (i18n)

## License

MIT
