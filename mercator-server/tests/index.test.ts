import StartApp from '../src/index';

test('test initialization of StartApp', () => {
    const app = new StartApp;
    expect(app.onInit()).toBe(true);
});