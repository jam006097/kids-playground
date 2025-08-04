import { MapManager } from '@mapManager';

describe('MapManager', () => {
  let mapManager;
  let mockMap;
  let mockTileLayer;
  let mockMarker;
  let mockDocumentQuerySelectorAll;
  let setTimeoutSpy;

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

    global.L = {
      map: jest.fn(() => mockMap),
      tileLayer: jest.fn(() => mockTileLayer),
      marker: jest.fn(() => mockMarker),
    };

    // DOM要素をモック
    mockDocumentQuerySelectorAll = jest.fn(() => [{
      getAttribute: jest.fn(name => {
        if (name === 'data-playground-id') return '1';
        return null;
      }),
      textContent: '',
    }, ]);
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
    setTimeoutSpy = jest.spyOn(global, 'setTimeout');

    mapManager = new MapManager();
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
    const mockPlaygrounds = [{
      id: '1',
      name: '公園A',
      address: '住所A',
      phone: '111',
      latitude: '31.5',
      longitude: '130.5'
    }, {
      id: '2',
      name: '公園B',
      address: '住所B',
      phone: '222',
      latitude: '31.6',
      longitude: '130.6'
    }, ];

    test('地図が初期化され、L.mapが適切な引数で呼び出されること', () => {
      mapManager.initMap(mockPlaygrounds);
      expect(global.L.map).toHaveBeenCalledWith('map-container');
      expect(mockMap.setView).toHaveBeenCalledWith(
        mapManager.KAGOSHIMA_CENTER,
        mapManager.DEFAULT_ZOOM_LEVEL,
      );
      expect(mockTileLayer.addTo).toHaveBeenCalledWith(window.mapInstance); // window.mapInstanceを渡す
    });

    test('遊び場が与えられた場合、各遊び場に対してマーカーが追加され、ポップアップがバインドされること', () => {
      mapManager.initMap(mockPlaygrounds);

      expect(global.L.marker).toHaveBeenCalledTimes(mockPlaygrounds.length);
      expect(mockMarker.addTo).toHaveBeenCalledTimes(mockPlaygrounds.length);
      expect(mockMarker.bindPopup).toHaveBeenCalledTimes(mockPlaygrounds.length);

      expect(global.L.marker).toHaveBeenCalledWith([31.5, 130.5]);
      expect(global.L.marker).toHaveBeenCalledWith([31.6, 130.6]);

      expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('公園A'));
      expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('公園B'));
    });

    test('window.mapInstanceが既に存在する場合、removeが呼び出されること', () => {
      global.window.mapInstance = mockMap;
      mapManager.initMap(mockPlaygrounds);
      expect(mockMap.remove).toHaveBeenCalled();
    });

    test('setTimeoutが呼び出されること', () => {
      mapManager.initMap(mockPlaygrounds);
      expect(setTimeoutSpy).toHaveBeenCalledTimes(1);
      expect(setTimeoutSpy).toHaveBeenCalledWith(expect.any(Function), 500);
    });
  });

  describe('initFavoritesMap', () => {
    const mockPlaygrounds = [{
      id: '1',
      name: 'お気に入り公園A',
      address: 'お気に入り住所A',
      phone: '333',
      latitude: '32.0',
      longitude: '131.0'
    }, ];

    test('お気に入り地図が初期化され、L.mapが適切な引数で呼び出されること', () => {
      mapManager.initFavoritesMap(mockPlaygrounds);
      expect(global.L.map).toHaveBeenCalledWith('mypage-map-container');
      expect(mockMap.setView).toHaveBeenCalledWith(
        mapManager.KAGOSHIMA_CENTER,
        mapManager.DEFAULT_ZOOM_LEVEL,
      );
      expect(mockTileLayer.addTo).toHaveBeenCalledWith(window.favMapInstance); // window.favMapInstanceを渡す
    });

    test('遊び場が与えられた場合、各遊び場に対してマーカーが追加され、ポップアップがバインドされること', () => {
      mapManager.initFavoritesMap(mockPlaygrounds);

      expect(global.L.marker).toHaveBeenCalledTimes(mockPlaygrounds.length);
      expect(mockMarker.addTo).toHaveBeenCalledTimes(mockPlaygrounds.length);
      expect(mockMarker.bindPopup).toHaveBeenCalledTimes(mockPlaygrounds.length);

      expect(global.L.marker).toHaveBeenCalledWith([32.0, 131.0]);
      expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('お気に入り公園A'));
    });

    test('window.favMapInstanceが既に存在する場合、removeが呼び出されること', () => {
      global.window.favMapInstance = mockMap;
      mapManager.initFavoritesMap(mockPlaygrounds);
      expect(mockMap.remove).toHaveBeenCalled();
    });
  });

  describe('updateFavoriteButtonsOnMap', () => {
    let mockButton1, mockButton2;

    beforeEach(() => {
      mockButton1 = {
        getAttribute: jest.fn(name => {
          if (name === 'data-playground-id') return '1';
          return null;
        }),
        textContent: '',
      };
      mockButton2 = {
        getAttribute: jest.fn(name => {
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
});
