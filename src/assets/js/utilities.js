const UtilitiesHandler = {
  install(Vue) {
    Vue.prototype.$util = {
      get timestampUTC() {
        return timestampUTC();
      },
      timestampWithOffset(timestamp) {
        return timestampWithOffset(timestamp);
      },
      humanReadableTime(timestamp) {
        return humanReadableTime(timestamp);
      }
    };
  }
};

export default UtilitiesHandler;

export const timestampUTC = () => {
  const now = new Date();
  return now.getTime() + now.getTimezoneOffset() * 60 * 1000;
};

export const timestampWithOffset = timestamp => {
  return timestamp - new Date().getTimezoneOffset() * 60 * 1000;
};

export const humanReadableTime = timestamp => {
  const date = new Date(timestampWithOffset(timestamp));
  return date.toTimeString().substr(0, 5);
};
