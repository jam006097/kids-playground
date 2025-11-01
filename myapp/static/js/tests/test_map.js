import { MapManager } from '../map.js';

describe('MapManager', () => {
  let mapManager;
  let mockMap;
  let mockTileLayer;
  let mockMarker;
  let mockL;
  let mockDocumentQuerySelectorAll;

  beforeEach(() => {
    // LeafletのLオブジェクトをモック
    mockMarker = {
      addTo: jest.fn().mockReturnThis(),
      bindPopup: jest.fn(),
    };
    mockTileLayer = {
      addTo: jest.fn().mockReturnThis(),
    };
    mockMap = {
      setView: jest.fn(),
      remove: jest.fn(),
      addLayer: jest.fn(),
    };

    mockL = {
      map: jest.fn(() => mockMap),
      tileLayer: jest.fn(() => mockTileLayer),
      marker: jest.fn(() => mockMarker),
    };

    // DOM要素をモック
    mockDocumentQuerySelectorAll = jest.fn(() => [
      {
        getAttribute: jest.fn((name) => {
          if (name === 'data-playground-id') return '1';
          return null;
        }),
        textContent: '',
      },
    ]);
    Object.defineProperty(global.document, 'querySelectorAll', {
      value: mockDocumentQuerySelectorAll,
      writable: true,
    });

    // windowオブジェクトのモック
    global.window.mapInstance = undefined;
    global.window.favMapInstance = undefined;
    global.window.favorite_ids = [];

    // setTimeoutをモック
    jest.useFakeTimers();

    mapManager = new MapManager(mockL);
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
    jest.restoreAllMocks(); // spyOnで作成したモックを元に戻す
  });

  test('MapManagerが正しく初期化されること', () => {
    expect(mapManager.KAGOSHIMA_CENTER).toEqual([31.5602, 130.5581]);
    expect(mapManager.DEFAULT_ZOOM_LEVEL).toBe(10);
  });

  describe('initMap', () => {
    const mockPlaygrounds = [
      { id: '1', latitude: '31.5', longitude: '130.5' },
      { id: '2', latitude: '31.6', longitude: '130.6' },
    ];

    test('地図を初期化し、遊び場のピンを配置すること', () => {
      mapManager.initMap(mockPlaygrounds);

      // 検証：地図が生成され、ピンが遊び場の数だけ作られようとしたか
      expect(mockL.map).toHaveBeenCalled();
      expect(mockL.marker).toHaveBeenCalledTimes(mockPlaygrounds.length);
    });

    test('地図が既に存在する場合、古い地図を破棄してから新しい地図を描画すること', () => {
      global.window.mapInstance = mockMap;
      mapManager.initMap(mockPlaygrounds);

      // 検証：古い地図のremoveが呼ばれたか
      expect(mockMap.remove).toHaveBeenCalled();
      // 検証：新しい地図が生成されたか
      expect(mockL.map).toHaveBeenCalled();
    });
  });

  describe('initFavoritesMap', () => {
    const mockPlaygrounds = [
      { id: '1', latitude: '32.0', longitude: '131.0' },
    ];

    test('お気に入り地図を初期化し、ピンを配置すること', () => {
      mapManager.initFavoritesMap(mockPlaygrounds);

      // 検証：地図が生成され、ピンが遊び場の数だけ作られようとしたか
      expect(mockL.map).toHaveBeenCalled();
      expect(mockL.marker).toHaveBeenCalledTimes(mockPlaygrounds.length);
    });

    test('お気に入り地図が既に存在する場合、古い地図を破棄してから新しい地図を描画すること', () => {
      global.window.favMapInstance = mockMap;
      mapManager.initFavoritesMap(mockPlaygrounds);

      // 検証：古い地図のremoveが呼ばれたか
      expect(mockMap.remove).toHaveBeenCalled();
      // 検証：新しい地図が生成されたか
      expect(mockL.map).toHaveBeenCalled();
    });
  });

  describe('updateFavoriteButtonsOnMap', () => {
    let mockButton1, mockButton2;

    beforeEach(() => {
      mockButton1 = {
        getAttribute: jest.fn((name) => {
          if (name === 'data-playground-id') return '1';
          return null;
        }),
        textContent: '',
      };
      mockButton2 = {
        getAttribute: jest.fn((name) => {
          if (name === 'data-playground-id') return '2';
          return null;
        }),
        textContent: '',
      };
      mockDocumentQuerySelectorAll.mockReturnValue([mockButton1, mockButton2]);
    });

    test('お気に入りIDに基づいてボタンのテキストが正しく更新されること', () => {
      const favoriteIds = ['1'];
      mapManager.updateFavoriteButtonsOnMap(favoriteIds);

      expect(mockButton1.textContent).toBe('お気に入り解除');
      expect(mockButton2.textContent).toBe('お気に入りに追加');
    });

    test('お気に入りIDが空の場合、すべてのボタンが「お気に入りに追加」になること', () => {
      const favoriteIds = [];
      mapManager.updateFavoriteButtonsOnMap(favoriteIds);

      expect(mockButton1.textContent).toBe('お気に入りに追加');
      expect(mockButton2.textContent).toBe('お気に入りに追加');
    });
  });

  describe('ポップアップ内のお気に入り状態の動的更新', () => {
    const mockPlayground = {
      id: '1',
      name: '公園A',
      address: '住所A',
      phone: '111',
      latitude: '31.5',
      longitude: '130.5',
    };

    test('お気に入り登録後、再度ポップアップを開くと状態が「お気に入り解除」に更新されていること', () => {
      // 1. 初期状態ではお気に入りではない
      window.favorite_ids = [];
      let popupContent = mapManager.createPopupContent(mockPlayground);
      expect(popupContent).toContain('お気に入りに追加');

      // 2. お気に入りに登録する（FavoriteManagerの動作を模倣）
      window.favorite_ids.push('1');

      // 3. 再度ポップアップの内容を生成すると、状態が更新されている
      popupContent = mapManager.createPopupContent(mockPlayground);
      expect(popupContent).toContain('お気に入り解除');
    });
  });
});
