function titleCaseMc(str) {
  if (!str) {
    return ""
  }

  return str.toLowerCase().replace(/(^|\s)(mc)(\w+)/g, (match, p1, p2, p3) => {
    return p1 + p2.charAt(0).toUpperCase() + p2.slice(1) + p3.charAt(0).toUpperCase() + p3.slice(1)
  }).replace(/(^|\s)(\w)/g, (match, p1, p2) => {
    return p1 + p2.toUpperCase()
  })
}