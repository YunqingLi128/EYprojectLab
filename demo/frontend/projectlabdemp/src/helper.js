export default {
  getQuarterList: function (quarterStart, quarterEnd) {
    let listStart = quarterStart.split(/[Q]/)
    let listEnd = quarterEnd.split(/[Q]/)
    let quarterFrom = parseInt(listStart[1])
    let quarterTo = parseInt(listEnd[1])
    let yearFrom = parseInt(listStart[0])
    let yearTo = parseInt(listEnd[0])
    let quarterList = []
    while (yearFrom <= yearTo) {
      quarterList.push(yearFrom.toString() + 'Q' + quarterFrom.toString())
      if (yearFrom === yearTo && quarterFrom === quarterTo) {
        break
      }
      quarterFrom += 1
      if (quarterFrom > 4) {
        quarterFrom = 1
        yearFrom += 1
      }
    }
    return quarterList
  }
}
