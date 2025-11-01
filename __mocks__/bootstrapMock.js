// __mocks__/bootstrapMock.js
module.exports = {
  Modal: jest.fn().mockImplementation(() => {
    return {
      hide: jest.fn(),
      show: jest.fn(),
    };
  }),
};
