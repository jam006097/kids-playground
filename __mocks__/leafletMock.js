const mockMap = {
    setView: jest.fn().mockReturnThis(),
    remove: jest.fn(),
};

const mockTileLayer = {
    addTo: jest.fn().mockReturnThis(),
};

const mockMarker = {
    addTo: jest.fn().mockReturnThis(),
    bindPopup: jest.fn().mockReturnThis(),
};

const L = {
    map: jest.fn(() => mockMap),
    tileLayer: jest.fn(() => mockTileLayer),
    marker: jest.fn(() => mockMarker),
};

export { L, mockMap, mockTileLayer, mockMarker };