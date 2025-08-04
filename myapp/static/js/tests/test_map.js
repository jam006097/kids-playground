import { MapManager } from '../map.js';
import { L, mockMap, mockTileLayer, mockMarker } from 'leaflet'; // Leafletのモックをインポート

describe('MapManager', () => {
    let mapManager;
    let mockPlaygrounds;

    beforeEach(() => {
        // Clear module cache to re-load map.js for each test
        jest.resetModules();
        const { MapManager } = require('../map.js'); // map.jsを再読み込み
        mapManager = new MapManager();
        mockPlaygrounds = [
            { id: '1', name: '公園A', address: '住所A', phone: '111', latitude: '31.5', longitude: '130.5' },
            { id: '2', name: '公園B', address: '住所B', phone: '222', latitude: '31.6', longitude: '130.6' },
        ];

        // window.mapInstanceとwindow.favMapInstanceをクリア
        window.mapInstance = undefined;
        window.favMapInstance = undefined;
        window.favorite_ids = []; // favorite_idsもクリア

        // Leafletのモックをグローバルに設定
        global.L = L; // Lはjest.mockで定義したモックオブジェクト

        // Leafletのモックをクリア
        L.map.mockClear();
        mockMap.setView.mockClear();
        mockMap.remove.mockClear();
        L.tileLayer.mockClear();
        mockTileLayer.addTo.mockClear();
        L.marker.mockClear();
        mockMarker.addTo.mockClear();
        mockMarker.bindPopup.mockClear();

        // DOM要素の準備
        document.body.innerHTML = `
            <div id="map-container" style="width: 100px; height: 100px;"></div>
            <div id="mypage-map-container" style="width: 100px; height: 100px;"></div>
            <button class="btn-outline-success" data-playground-id="1">お気に入りに追加</button>
            <button class="btn-outline-success" data-playground-id="2">お気に入りに追加</button>
        `;
    });

    // シナリオ: initMapが地図を初期化し、マーカーを追加する
    test('initMapが地図を初期化し、マーカーを追加する', () => {
        mapManager.initMap(mockPlaygrounds);

        // 検証: L.mapが正しいコンテナIDとビュー設定で呼び出されたこと
        expect(L.map).toHaveBeenCalledWith('map-container');
        expect(mockMap.setView).toHaveBeenCalledWith(mapManager.KAGOSHIMA_CENTER, mapManager.DEFAULT_ZOOM_LEVEL);

        // 検証: L.tileLayerが呼び出され、地図に追加されたこと
        expect(L.tileLayer).toHaveBeenCalledWith('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', expect.any(Object));
        expect(mockTileLayer.addTo).toHaveBeenCalledWith(mockMap);

        // 検証: 各プレイグラウンドに対してL.markerが呼び出され、地図に追加されたこと
        expect(L.marker).toHaveBeenCalledTimes(mockPlaygrounds.length);
        expect(mockMarker.addTo).toHaveBeenCalledTimes(mockPlaygrounds.length);

        // 検証: マーカーのポップアップが正しい内容でバインドされたこと
        expect(mockMarker.bindPopup).toHaveBeenCalledTimes(mockPlaygrounds.length);
        expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('公園A'));
        expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('公園B'));
    });

    // シナリオ: initMapが既存の地図インスタンスを削除する
    test('initMapが既存の地図インスタンスを削除する', () => {
        window.mapInstance = mockMap; // 既存のインスタンスをモックに設定
        mapManager.initMap(mockPlaygrounds);
        expect(mockMap.remove).toHaveBeenCalled();
    });

    // シナリオ: initFavoritesMapが地図を初期化し、マーカーを追加する
    test('initFavoritesMapが地図を初期化し、マーカーを追加する', () => {
        mapManager.initFavoritesMap(mockPlaygrounds);

        // 検証: L.mapが正しいコンテナIDとビュー設定で呼び出されたこと
        expect(L.map).toHaveBeenCalledWith('mypage-map-container');
        expect(mockMap.setView).toHaveBeenCalledWith(mapManager.KAGOSHIMA_CENTER, mapManager.DEFAULT_ZOOM_LEVEL);

        // 検証: L.tileLayerが呼び出され、地図に追加されたこと
        expect(L.tileLayer).toHaveBeenCalledWith('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', expect.any(Object));
        expect(mockTileLayer.addTo).toHaveBeenCalledWith(mockMap);

        // 検証: 各プレイグラウンドに対してL.markerが呼び出され、地図に追加されたこと
        expect(L.marker).toHaveBeenCalledTimes(mockPlaygrounds.length);
        expect(mockMarker.addTo).toHaveBeenCalledTimes(mockPlaygrounds.length);

        // 検証: マーカーのポップアップが正しい内容でバインドされたこと
        expect(mockMarker.bindPopup).toHaveBeenCalledTimes(mockPlaygrounds.length);
        expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('公園A'));
        expect(mockMarker.bindPopup).toHaveBeenCalledWith(expect.stringContaining('公園B'));
    });

    // シナリオ: initFavoritesMapが既存のお気に入り地図インスタンスを削除する
    test('initFavoritesMapが既存のお気に入り地図インスタンスを削除する', () => {
        window.favMapInstance = mockMap; // 既存のインスタンスをモックに設定
        mapManager.initFavoritesMap(mockPlaygrounds);
        expect(mockMap.remove).toHaveBeenCalled();
    });

    // シナリオ: updateFavoriteButtonsOnMapがボタンのテキストを更新する
    test('updateFavoriteButtonsOnMapがボタンのテキストを更新する', () => {
        // 準備: お気に入りIDのリスト
        window.favorite_ids = ['1'];

        // 実行: updateFavoriteButtonsOnMapを呼び出す
        mapManager.updateFavoriteButtonsOnMap(window.favorite_ids);

        // 検証: ボタンのテキストが正しく更新されたこと
        const button1 = document.querySelector('[data-playground-id="1"]');
        const button2 = document.querySelector('[data-playground-id="2"]');

        expect(button1.textContent).toBe('お気に入り解除');
        expect(button2.textContent).toBe('お気に入りに追加');
    });
});