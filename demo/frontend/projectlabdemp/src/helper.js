export default {
  getLatestQuarter () {
    // TODO: hard-coded currently
    return '2020Q4'
  },
  getDefaultStartQuarter () {
    // Use latest year - 1 as the default start year
    let latest = this.getLatestQuarter()
    let parts = latest.split(/[Q]/)
    let year = parseInt(parts[0])
    let quarter = parseInt(parts[1])
    return (year - 1).toString() + 'Q' + quarter.toString()
  },
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
