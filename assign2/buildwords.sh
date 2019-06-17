#!/bin/bash

#remove '?'
sed 's/?//g' | 

#remove <u> and </u> tags 
sed 's/<\/\?u>//g' |

#make all characters lowercase
tr '[:upper:]' '[:lower:]' |

#take only lines of the form "A<tdX>W</td>Z"
grep ' *<td[^>]*>[pk`mnwlhaeiou ]*</td> *' |

#remove HTML tags
sed 's/<[^>]*>//g' |

#treat ` as '
tr '`' "'" |

#replace all non-Hawaiian chars with newline chars
tr -c "pk'mnwlhaeiou" '[\n*]' |

#erase all whitespace
tr -d '[:blank:]' |

sort -u | 

#remove empty lines
sed '/^ *$/d'
