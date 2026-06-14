// Traditional Catholic prayers (public domain texts).
const PRAYERS = [
  {
    id: 'morning-offering',
    title: 'Morning Offering',
    group: 'Morning',
    text: `O Jesus, through the Immaculate Heart of Mary, I offer You my prayers, works, joys, and sufferings of this day for all the intentions of Your Sacred Heart, in union with the Holy Sacrifice of the Mass throughout the world, in thanksgiving for Your favors, in reparation for my sins, and for all the intentions of our associates, and in particular for the intentions of the Holy Father this month.

Amen.`
  },
  {
    id: 'sign-of-the-cross',
    title: 'Sign of the Cross',
    group: 'Morning',
    text: `In the name of the Father, and of the Son, and of the Holy Spirit.

Amen.`
  },
  {
    id: 'our-father',
    title: "The Lord's Prayer (Our Father)",
    group: 'Core Prayers',
    text: `Our Father, who art in heaven, hallowed be Thy name. Thy kingdom come, Thy will be done, on earth as it is in heaven. Give us this day our daily bread, and forgive us our trespasses, as we forgive those who trespass against us. And lead us not into temptation, but deliver us from evil.

Amen.`
  },
  {
    id: 'hail-mary',
    title: 'Hail Mary',
    group: 'Core Prayers',
    text: `Hail Mary, full of grace, the Lord is with thee. Blessed art thou among women, and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death.

Amen.`
  },
  {
    id: 'glory-be',
    title: 'Glory Be (Doxology)',
    group: 'Core Prayers',
    text: `Glory be to the Father, and to the Son, and to the Holy Spirit. As it was in the beginning, is now, and ever shall be, world without end.

Amen.`
  },
  {
    id: 'apostles-creed',
    title: "The Apostles' Creed",
    group: 'Core Prayers',
    text: `I believe in God, the Father almighty, Creator of heaven and earth, and in Jesus Christ, His only Son, our Lord, who was conceived by the Holy Spirit, born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died, and was buried; He descended into hell; on the third day He rose again from the dead; He ascended into heaven, and is seated at the right hand of God the Father almighty; from there He will come to judge the living and the dead.

I believe in the Holy Spirit, the holy catholic Church, the communion of saints, the forgiveness of sins, the resurrection of the body, and life everlasting.

Amen.`
  },
  {
    id: 'act-of-contrition',
    title: 'Act of Contrition',
    group: 'Penance',
    text: `O my God, I am heartily sorry for having offended Thee, and I detest all my sins because of Thy just punishments, but most of all because they offend Thee, my God, who art all-good and deserving of all my love. I firmly resolve, with the help of Thy grace, to sin no more and to avoid the near occasions of sin.

Amen.`
  },
  {
    id: 'memorare',
    title: 'The Memorare',
    group: 'Marian Prayers',
    text: `Remember, O most gracious Virgin Mary, that never was it known that anyone who fled to your protection, implored your help, or sought your intercession was left unaided.

Inspired with this confidence, I fly unto you, O Virgin of virgins, my Mother. To you do I come, before you I stand, sinful and sorrowful. O Mother of the Word Incarnate, despise not my petitions, but in your mercy hear and answer me.

Amen.`
  },
  {
    id: 'st-michael',
    title: 'Prayer to St. Michael the Archangel',
    group: 'Protection',
    text: `St. Michael the Archangel, defend us in battle. Be our protection against the wickedness and snares of the devil. May God rebuke him, we humbly pray, and do thou, O Prince of the Heavenly Host, by the power of God, cast into hell Satan and all the evil spirits who prowl about the world seeking the ruin of souls.

Amen.`
  },
  {
    id: 'angelus',
    title: 'The Angelus',
    group: 'Marian Prayers',
    text: `V. The Angel of the Lord declared unto Mary.
R. And she conceived of the Holy Spirit.
Hail Mary, full of grace...

V. Behold the handmaid of the Lord.
R. Be it done unto me according to Thy word.
Hail Mary, full of grace...

V. And the Word was made flesh.
R. And dwelt among us.
Hail Mary, full of grace...

V. Pray for us, O Holy Mother of God.
R. That we may be made worthy of the promises of Christ.

Let us pray: Pour forth, we beseech Thee, O Lord, Thy grace into our hearts, that we, to whom the Incarnation of Christ, Thy Son, was made known by the message of an angel, may by His Passion and Cross be brought to the glory of His Resurrection, through the same Christ our Lord.

Amen.`
  },
  {
    id: 'grace-before-meals',
    title: 'Grace Before Meals',
    group: 'Daily Life',
    text: `Bless us, O Lord, and these Thy gifts, which we are about to receive from Thy bounty, through Christ our Lord.

Amen.`
  },
  {
    id: 'grace-after-meals',
    title: 'Grace After Meals',
    group: 'Daily Life',
    text: `We give Thee thanks for all Thy benefits, O Almighty God, who livest and reignest world without end.

Amen.`
  },
  {
    id: 'evening-examen',
    title: 'Evening Examen (Guided Review)',
    group: 'Evening',
    text: `Before sleep, spend a few quiet minutes reviewing the day with God:

1. Gratitude — Recall the day and give thanks for its gifts, however small.
2. Review — Look back over the day, hour by hour, noticing where you felt close to God and where you didn't.
3. Sorrow — Acknowledge moments of failure or sin, and ask for forgiveness.
4. Hope — Look ahead to tomorrow, asking for the grace to live it well.

Close with an Our Father or Glory Be.`
  },
  {
    id: 'guardian-angel',
    title: 'Guardian Angel Prayer',
    group: 'Protection',
    text: `Angel of God, my guardian dear, to whom God's love commits me here, ever this day be at my side, to light and guard, to rule and guide.

Amen.`
  }
];
