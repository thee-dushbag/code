function sleep(delay, callback_value, ...args) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      try {
        if (typeof callback_value === 'function')
          resolve(callback_value(...args))
        else if (args.length > 0)
          resolve([callback_value, ...args])
        else
          resolve(callback_value)
      } catch (error) {
        reject(error)
      }
    }, delay * 1000);
  })
}

export { sleep }